from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from madr.database import get_async_session

T_Session = Annotated[Session, Depends(get_async_session)]
