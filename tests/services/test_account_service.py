from http import HTTPStatus

import pytest
from fastapi import HTTPException

from madr.schemas.account import AccountSchema
from madr.services.account_service import AccountService


@pytest.mark.asyncio
async def test_create_account_success(session, faker):
    account_service = AccountService(session)
    account_data = AccountSchema(
        username=faker.user_name(),
        email=faker.email(),
        password=faker.password(),
    )

    result = await account_service.create_account(account_data)

    assert result.username == account_data.username
    assert result.email == account_data.email


@pytest.mark.asyncio
async def test_create_account_username_exists(session, user):
    account_service = AccountService(session)
    account_data = AccountSchema(
        username=user.username,
        email="new_email@test.com",
        password="password123",
    )

    with pytest.raises(HTTPException) as exc_info:
        await account_service.create_account(account_data)

    assert exc_info.value.status_code == HTTPStatus.CONFLICT
    assert exc_info.value.detail == "Username already exists"


@pytest.mark.asyncio
async def test_create_account_email_exists(session, user):
    account_service = AccountService(session)
    account_data = AccountSchema(
        username="new_username",
        email=user.email,
        password="password123",
    )

    with pytest.raises(HTTPException) as exc_info:
        await account_service.create_account(account_data)

    assert exc_info.value.status_code == HTTPStatus.CONFLICT
    assert exc_info.value.detail == "Email already exists"


@pytest.mark.asyncio
async def test_list_accounts(session, user):
    account_service = AccountService(session)

    result = await account_service.list_accounts()

    assert len(result["users"]) > 0
    assert any(account.username == user.username for account in result["users"])


@pytest.mark.asyncio
async def test_get_account_by_id_success(session, user):
    account_service = AccountService(session)

    result = await account_service.get_account_by_id(user.id)

    assert result.id == user.id
    assert result.username == user.username


@pytest.mark.asyncio
async def test_get_account_by_id_not_found(session):
    account_service = AccountService(session)

    with pytest.raises(HTTPException) as exc_info:
        await account_service.get_account_by_id(999)

    assert exc_info.value.status_code == HTTPStatus.NOT_FOUND
    assert exc_info.value.detail == "User not found"


@pytest.mark.asyncio
async def test_update_account_success(session, user, token):
    account_service = AccountService(session)
    account_data = AccountSchema(
        username="updated_username",
        email="updated_email@test.com",
        password="new_password",
    )

    result = await account_service.update_account(user.id, account_data, user)

    assert result.username == account_data.username
    assert result.email == account_data.email


@pytest.mark.asyncio
async def test_update_account_forbidden(session, user, other_user):
    account_service = AccountService(session)
    account_data = AccountSchema(
        username="updated_username",
        email="updated_email@test.com",
        password="new_password",
    )

    with pytest.raises(HTTPException) as exc_info:
        await account_service.update_account(user.id, account_data, other_user)

    assert exc_info.value.status_code == HTTPStatus.FORBIDDEN
    assert exc_info.value.detail == "Not enough permissions"


@pytest.mark.asyncio
async def test_delete_account_success(session, user):
    account_service = AccountService(session)

    result = await account_service.delete_account(user.id, user)

    assert result["message"] == "User deleted successfully"


@pytest.mark.asyncio
async def test_delete_account_forbidden(session, user, other_user):
    account_service = AccountService(session)

    with pytest.raises(HTTPException) as exc_info:
        await account_service.delete_account(user.id, other_user)

    assert exc_info.value.status_code == HTTPStatus.FORBIDDEN
    assert exc_info.value.detail == "Not enough permissions"
