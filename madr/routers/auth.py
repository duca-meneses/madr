
from fastapi import APIRouter

from madr.config.security import create_access_token
from madr.schemas.auth import AuthPassword, Token
from madr.schemas.message import MessageSchema
from madr.services.auth_service import AuthService
from madr.utils.dependencies import T_CurrentUser, T_FormData, T_Session

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token', response_model=Token)
async def login(session: T_Session, form_data: T_FormData):
    service = AuthService(session=session, form_data=form_data)

    token = await service.login_for_access_token()

    return token


@router.post('/refresh-token', response_model=Token)
async def refresh_token(user: T_CurrentUser):
    access_token = create_access_token(
        data={'name': user.username, 'sub': user.email, 'user_id': user.id}
    )

    return {'access_token': access_token, 'token_type': 'Bearer'}


@router.post('/password/change', response_model=MessageSchema)
async def update_password(
    user: T_CurrentUser, auth_password: AuthPassword, session: T_Session
):
    service = AuthService(session=session)
    response = await service.update_password(user=user, auth_password=auth_password)

    return response
