from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class AccountSchema(BaseModel):
    username: Annotated[
        str,
        Field(description='username of the user', max_length=25, min_length=3),
    ]
    email: Annotated[EmailStr, Field(description='email of the user')]
    password: Annotated[str, Field(
        description='password of the user',
        min_length=8,
        max_length=100,
        examples=['string12'],
        )
    ]


class AccountPublic(BaseModel):
    id: Annotated[int, Field(description='ID of the user')]
    email: Annotated[EmailStr, Field(description='email of the user')]
    username: Annotated[str, Field(description='username of the user')]

    model_config = ConfigDict(from_attributes=True)


class AccountUpdateSchema(BaseModel):
    username: Optional[Annotated[
        str,
        Field(description='username of the user', max_length=25, min_length=3),
        ]
    ]
    email: Optional[Annotated[EmailStr, Field(description='email of the user')]]


class AccountList(BaseModel):
    users: list[AccountPublic]
