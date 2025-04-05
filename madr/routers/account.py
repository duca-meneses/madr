from http import HTTPStatus

from fastapi import APIRouter

from madr.schemas.account import (
    AccountList,
    AccountPublic,
    AccountSchema,
)
from madr.schemas.message import MessageSchema
from madr.services.account_service import AccountService
from madr.utils.dependencies import T_CurrentUser, T_Session

router = APIRouter(prefix='/users', tags=['account'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=AccountPublic)
async def create_account(account: AccountSchema, session: T_Session):
    service = AccountService(session)
    return await service.create_account(account)


@router.get('/', response_model=AccountList, status_code=HTTPStatus.OK)
async def list_accounts(session: T_Session, limit: int = 10, skip: int = 0):
    service = AccountService(session)
    return await service.list_accounts(limit, skip)


@router.get(
    '/{user_id}', response_model=AccountPublic, status_code=HTTPStatus.OK
)
async def get_account_by_id(user_id: int, session: T_Session):
    service = AccountService(session)
    return await service.get_account_by_id(user_id)


@router.put(
    '/{user_id}', response_model=AccountPublic, status_code=HTTPStatus.OK
)
async def update_account(
    user_id: int,
    account: AccountSchema,
    session: T_Session,
    current_user: T_CurrentUser
):
    service = AccountService(session)
    return await service.update_account(user_id, account, current_user)


@router.delete(
    '/{user_id}', response_model=MessageSchema, status_code=HTTPStatus.OK
)
async def delete_account(user_id: int, session: T_Session, current_user: T_CurrentUser):
    service = AccountService(session)
    return await service.delete_account(user_id, current_user)
