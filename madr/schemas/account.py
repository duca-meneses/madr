from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class AccountSchema(BaseModel):
    username: Annotated[str, Field(
        description='username of the user', max_length=25, min_length=3)
    ]
    email: Annotated[EmailStr, Field(description='email of the user')]
    password: Annotated[str, Field(description='password of the user')]


class AccountPublic(BaseModel):
    id: Annotated[int, Field(description='ID of the user')]
    email: Annotated[EmailStr, Field(description='email of the user')]
    username: Annotated[str, Field(
        description='username of the user')]

    model_config = ConfigDict(from_attributes=True)


class AccountList(BaseModel):
    users: list[AccountPublic]
