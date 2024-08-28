from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio.session import AsyncSession

from madr.config.security import get_current_user
from madr.data.database import get_async_session
from madr.data.models import Account

T_Session = Annotated[AsyncSession, Depends(get_async_session)]
T_CurrentUser = Annotated[Account, Depends(get_current_user)]
T_FormData = Annotated[OAuth2PasswordRequestForm, Depends()]
