from typing import Annotated

from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: Annotated[str, Field(description='access JWt token')]
    token_type: Annotated[str, Field(description='type of token')]


class TokenData(BaseModel):
    username: str | None = None
