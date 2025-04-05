
from functools import cache
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select

from madr.config.security import get_password_hash
from madr.data.models import Account
from madr.schemas.account import AccountSchema
from madr.utils.dependencies import T_CurrentUser, T_Session


@cache
class AccountService():
    def __init__(self, session: T_Session):
        self.session = session

    async def create_account(self, account: AccountSchema):
        db_account = await self.session.scalar(
        select(Account).where(
            (Account.username == account.username)
            | (Account.email == account.email)
        )
    )

        if db_account:
            if db_account.username == account.username:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT,
                    detail='Username already exists',
                )
            elif db_account.email == account.email:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT, detail='Email already exists'
                )

        db_account = Account(
            username=account.username,
            email=account.email,
            password=get_password_hash(account.password),
        )

        self.session.add(db_account)
        await self.session.commit()
        await self.session.refresh(db_account)

        return db_account

    async def list_accounts(self, limit: int = 10, skip: int = 0):
        accounts = await self.session.scalars(
            select(Account).limit(limit).offset(skip)
        )
        return {'users': list(accounts)}

    async def get_account_by_id(self, user_id: int):
        account = await self.session.scalar(
            select(Account).where(Account.id == user_id)
        )
        if not account:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='User not found'
            )
        return account

    async def update_account(
        self,
        user_id: int,
        account: AccountSchema,
        current_user: T_CurrentUser,
    ):
        if current_user.id != user_id:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
            )

        current_user.email = account.email
        current_user.username = account.username

        await self.session.commit()
        await self.session.refresh(current_user)
        return current_user

    async def delete_account(self, user_id: int, current_user: T_CurrentUser):
        if current_user.id != user_id:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
            )
        await self.session.delete(current_user)
        await self.session.commit()
        return {'message': 'User deleted successfully'}
