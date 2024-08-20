from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from madr.dependencies import T_Session
from madr.models import Account
from madr.schemas import (
    AccountList,
    AccountPublic,
    AccountSchema,
    MessageSchema,
)

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=AccountPublic)
async def create_account(account: AccountSchema, session: T_Session):
    db_account = await session.scalar(
        select(Account).where(
            (Account.username == account.username) |
            (Account.email == account.email)
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
        password=account.password,
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
    user_id: int, account: AccountSchema, session: T_Session
):
    account_db = await session.scalar(
        select(Account).where(Account.id == user_id)
    )
    if not account_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    account_db.email = account.email
    account_db.username = account.username
    account_db.password = account.password

    await session.commit()
    await session.refresh(account_db)

    return account_db


@router.delete(
    '/{user_id}', response_model=MessageSchema, status_code=HTTPStatus.OK
)
async def delete_account(user_id: int, session: T_Session):
    account_db = await session.scalar(
        select(Account).where(Account.id == user_id)
    )

    if not account_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    await session.delete(account_db)
    await session.commit()

    return {'message': 'User deleted successfully'}
