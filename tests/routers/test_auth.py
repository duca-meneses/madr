from http import HTTPStatus

from freezegun import freeze_time
from httpx import AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession

from madr.data.models import Account


async def test_get_token(client: AsyncClient, user: Account):
    response = await client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


async def test_login_for_access_token_incorrect_credentials(
    client: AsyncClient, session: AsyncSession
):
    response = await client.post(
        'auth/token',
        data={'username': 'wrong@email.com', 'password': 'wrong_password'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


async def test_token_wrong_password(client: AsyncClient, user: Account):
    response = await client.post(
        'auth/token',
        data={'username': user.email, 'password': 'wrong_password'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


async def test_token_wrong_email(client: AsyncClient, user: Account):
    response = await client.post(
        'auth/token',
        data={'username': 'wrong@email.com', 'password': user.clean_password},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


async def test_refresh_token(client: AsyncClient, token):
    response = await client.post(
        'auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'Bearer'


async def test_token_expired_dont_refresh(client: AsyncClient, user: Account):
    with freeze_time('2023-07-14 12:00:00'):
        response = await client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-07-14 13:01:00'):
        response = await client.post(
            '/auth/refresh_token', headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Not authorized'}
