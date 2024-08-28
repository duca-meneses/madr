from http import HTTPStatus

import pytest
from fastapi import HTTPException
from freezegun import freeze_time
from httpx import AsyncClient
from jwt import decode
from sqlalchemy.ext.asyncio.session import AsyncSession

from madr.config.security import (
    create_access_token,
    get_current_user,
    settings,
)
from madr.data.models import Account


async def test_jwt():
    data = {'sub': 'test@test.com'}
    token = create_access_token(data)

    result = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert result['sub'] == data['sub']
    assert result['exp']


async def test_jwt_invalid_token(client: AsyncClient):
    response = await client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authorized'}


async def test_get_current_user_missing_username(
    session: AsyncSession, user: Account
):
    token = create_access_token(data={'bup': user.email})

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(session, token)

    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED


async def test_get_current_user_without_user(session: AsyncSession):
    user_fake = Account(
        username='fake', email='fake@test.com', password='fake'
    )
    token = create_access_token(data={'sub': user_fake.email})

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(session, token)

    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED


async def test_token_expired_after_time(client: AsyncClient, user: Account):
    with freeze_time('2024-08-20 12:00:00'):
        response = await client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password}
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2024-08-20 13:01:00'):
        response = await client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'wrong',
                'email': 'wrong@example.com',
                'password': 'wrong',
            }
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Not authorized'}
