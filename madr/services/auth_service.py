from functools import cache
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select

from madr.config.security import create_access_token, get_password_hash, verify_password
from madr.data.models import Account
from madr.schemas.auth import AuthPassword, Token
from madr.schemas.message import MessageSchema
from madr.utils.dependencies import T_CurrentUser, T_FormData, T_Session


@cache
class AuthService:
    def __init__(self, session: T_Session = None, form_data: T_FormData = None):
        self.session = session
        self.form_data = form_data

    async def login_for_access_token(self):

        user = await self.session.scalar(
        select(Account).where(Account.email == self.form_data.username)
        )

        if not user or not verify_password(self.form_data.password, user.password):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Incorrect email or password',
            )

        access_token = create_access_token(
            data={'name': user.username, 'sub': user.email, 'user_id': user.id}
        )

        return Token(access_token=access_token, token_type='Bearer')

    async def update_password(self, user: T_CurrentUser, auth_password: AuthPassword):
        if not verify_password(auth_password.password, user.password):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Incorrect password',
            )
        if auth_password.new_password != auth_password.confirm_new_password:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='New password and confirm new password do not match',
            )
        user.password = get_password_hash(auth_password.new_password)
        await self.session.commit()
        await self.session.refresh(user)

        return MessageSchema(message='Password updated successfully')
