from http import HTTPStatus

import pytest
from faker import Faker
from httpx import AsyncClient

from madr.data.models import Account
from madr.schemas.account import AccountPublic


@pytest.mark.asyncio
async def test_create_account(client: AsyncClient, faker: Faker):
    expect = {'username': faker.name_nonbinary(), 'email': faker.email()}

    response = await client.post(
        '/users/',
        json=expect | {'password': faker.password()},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == expect | {'id': 1}


@pytest.mark.asyncio
async def test_create_user_with_already_existing_username(
    client: AsyncClient, faker: Faker, user: Account
):
    response = await client.post(
        '/users/',
        json={
            'username': user.username,
            'email': faker.email(),
            'password': faker.password(),
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


@pytest.mark.asyncio
async def test_create_user_with_already_existing_email(
    client: AsyncClient, faker: Faker, user: Account
):
    response = await client.post(
        '/users/',
        json={
            'username': faker.name_nonbinary(),
            'email': user.email,
            'password': faker.password(),
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


@pytest.mark.asyncio
async def test_read_account_without_data(client: AsyncClient):
    response = await client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


@pytest.mark.asyncio
async def test_read_account_with_data(client: AsyncClient, user: Account):
    account = AccountPublic.model_validate(user).model_dump()

    response = await client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [account]}


@pytest.mark.asyncio
async def test_get_account_by_id(client: AsyncClient, user):
    response = await client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }


@pytest.mark.asyncio
async def test_get_by_id_without_account(client):
    response = await client.get('/users/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


@pytest.mark.asyncio
async def test_update_account(client: AsyncClient, user: Account, token):
    response = await client.put(
        f'/users/{user.id}',
        json={
            'username': 'test2username',
            'email': 'test2@email.com',
            'password': 'test2password',
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'test2username',
        'email': 'test2@email.com',
        'id': 1,
    }


@pytest.mark.asyncio
async def test_update_account_not_found(client: AsyncClient, user):
    response = await client.put(
        '/users/999',
        json={
            'username': 'test2username',
            'email': 'test2@email.com',
            'password': 'test2password',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


@pytest.mark.asyncio
async def test_update_account_not_enough_permissions(
    client: AsyncClient, other_user: Account, token
):
    response = await client.put(
        f'/users/{other_user.id}',
        json={
            'username': 'new',
            'email': 'new@test.com',
            'password': 'newpassword',
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


@pytest.mark.asyncio
async def test_delete_account(client: AsyncClient, user: Account, token):
    response = await client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'}
        )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted successfully'}


@pytest.mark.asyncio
async def test_delete_without_account(client: AsyncClient):
    response = await client.delete('/users/1')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


@pytest.mark.asyncio
async def test_delete_account_not_enough_permissions(
    client: AsyncClient, other_user: Account, token
):
    response = await client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
