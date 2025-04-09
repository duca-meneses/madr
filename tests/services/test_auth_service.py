from http import HTTPStatus

import pytest
from fastapi import HTTPException

from madr.schemas.auth import AuthPassword
from madr.schemas.message import MessageSchema
from madr.services.auth_service import AuthService


@pytest.mark.asyncio
async def test_login_for_access_token_success(session, faker, user):
    form_data = type('FormData', (object,), {
        'username': user.email,
        'password': user.clean_password
    })()

    auth_service = AuthService(session=session, form_data=form_data)
    token = await auth_service.login_for_access_token()

    assert token.token_type == 'Bearer'
    assert token.access_token is not None


@pytest.mark.asyncio
async def test_login_for_access_token_invalid_credentials(session, faker):
    form_data = type('FormData', (object,), {
        'username': faker.email(),
        'password': faker.password()
    })()

    auth_service = AuthService(session=session, form_data=form_data)

    with pytest.raises(HTTPException) as exc_info:
        await auth_service.login_for_access_token()

    assert exc_info.value.status_code == HTTPStatus.BAD_REQUEST
    assert exc_info.value.detail == 'Incorrect email or password'


@pytest.mark.asyncio
async def test_update_password_success(session, user):
    auth_password = AuthPassword(
        password=user.clean_password,
        new_password='new_secure_password',
        confirm_new_password='new_secure_password'
    )

    auth_service = AuthService(session=session)
    response = await auth_service.update_password(user, auth_password)

    assert response == MessageSchema(message='Password updated successfully')
    assert user.password != user.clean_password  # Password should be hashed


@pytest.mark.asyncio
async def test_update_password_incorrect_current_password(session, user):
    auth_password = AuthPassword(
        password='wrong_password',
        new_password='new_secure_password',
        confirm_new_password='new_secure_password'
    )

    auth_service = AuthService(session=session)

    with pytest.raises(HTTPException) as exc_info:
        await auth_service.update_password(user, auth_password)

    assert exc_info.value.status_code == HTTPStatus.BAD_REQUEST
    assert exc_info.value.detail == 'Incorrect password'


@pytest.mark.asyncio
async def test_update_password_mismatch_new_password(session, user):
    auth_password = AuthPassword(
        password=user.clean_password,
        new_password='new_secure_password',
        confirm_new_password='different_password'
    )

    auth_service = AuthService(session=session)

    with pytest.raises(HTTPException) as exc_info:
        await auth_service.update_password(user, auth_password)

    assert exc_info.value.status_code == HTTPStatus.BAD_REQUEST
    assert exc_info.value.detail == 'New password and confirm new password do not match'
