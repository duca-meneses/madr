from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from madr.config.security import get_password_hash
from madr.data.models import Account
from madr.schemas.account import (
    AccountList,
    AccountPublic,
    AccountSchema,
)
from madr.schemas.message import MessageSchema
from madr.utils.dependencies import T_CurrentUser, T_Session

router = APIRouter(prefix='/users', tags=['account'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=AccountPublic)
async def create_account(account: AccountSchema, session: T_Session):
    db_account = await session.scalar(
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

    session.add(db_account)
    await session.commit()
    await session.refresh(db_account)

    return db_account


@router.get('/', response_model=AccountList, status_code=HTTPStatus.OK)
async def list_accounts(session: T_Session, limit: int = 10, skip: int = 0):
    accounts = await session.scalars(select(Account).limit(limit).offset(skip))
    return {'users': accounts}


@router.get(
    '/{user_id}', response_model=AccountPublic, status_code=HTTPStatus.OK
)
async def get_account_by_id(user_id: int, session: T_Session):
    account = await session.scalar(
        select(Account).where(Account.id == user_id)
    )

    if not account:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    return account


@router.put(
    '/{user_id}', response_model=AccountPublic, status_code=HTTPStatus.OK
)
async def update_account(
    user_id: int,
    account: AccountSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    current_user.email = account.email
    current_user.username = account.username
    current_user.password = get_password_hash(account.password)

    await session.commit()
    await session.refresh(current_user)

    return current_user


@router.delete(
    '/{user_id}', response_model=MessageSchema, status_code=HTTPStatus.OK
)
async def delete_account(
    user_id: int, session: T_Session, current_user: T_CurrentUser
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    await session.delete(current_user)
    await session.commit()

    return {'message': 'User deleted successfully'}
