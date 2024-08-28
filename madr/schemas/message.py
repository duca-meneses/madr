from typing import Annotated

from pydantic import BaseModel, Field


class MessageSchema(BaseModel):
    message: Annotated[str, Field('message of response')]
