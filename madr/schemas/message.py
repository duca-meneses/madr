from typing import Annotated, Optional

from pydantic import BaseModel, Field


class MessageSchema(BaseModel):
    message: Optional[Annotated[
        str,
        Field(title='message', description='message to response')
        ]
    ]
