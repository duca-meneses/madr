from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio.session import AsyncSession

from madr.database import get_async_session
from madr.models import Account
from madr.security import get_current_user

T_Session = Annotated[AsyncSession, Depends(get_async_session)]
T_CurrentUser = Annotated[Account, Depends(get_current_user)]
T_FormData = Annotated[OAuth2PasswordRequestForm, Depends()]
