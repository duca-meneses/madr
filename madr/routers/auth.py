from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from madr.config.security import create_access_token, verify_password
from madr.data.models import Account
from madr.schemas.auth import Token
from madr.utils.dependencies import T_CurrentUser, T_FormData, T_Session

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token', response_model=Token)
async def login_for_access_token(
    session: T_Session,
    form_data: T_FormData
):
    user = await session.scalar(
        select(Account).where(Account.email == form_data.username)
    )

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}


@router.post('/refresh_token', response_model=Token)
async def refresh_token(user: T_CurrentUser):
    new_access_token = create_access_token(data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'Bearer'}
