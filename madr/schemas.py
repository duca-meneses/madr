
from pydantic import BaseModel


class AccountSchema(BaseModel):
    username: str
    email: str
    password: str


class AccountPublic(BaseModel):
    id: int
    email: str
    username: str


class AccountList(BaseModel):
    users: list[AccountPublic]


class MessageSchema(BaseModel):
    message: str
