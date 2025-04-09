from typing import Annotated

from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: Annotated[str, Field(description='access JWt token')]
    token_type: Annotated[str, Field(description='type of token')]


class TokenData(BaseModel):
    username: str | None = None


class AuthPassword(BaseModel):
    password: str = Field(
        ...,
        title='Password',
        description='Current password to update',
        min_length=6,
        max_length=100,
        examples=['string'],
    )
    new_password: str = Field(
        ...,
        title='New Password',
        description='New password to update',
        min_length=8,
        max_length=100,
        examples=['string@1'],
    )
    confirm_new_password: str = Field(
        ...,
        title='Confirm new Password',
        description='Confirm new password',
        min_length=8,
        max_length=100,
        examples=['string@1'],
    )
