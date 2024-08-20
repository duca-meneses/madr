from pydantic import BaseModel, ConfigDict, EmailStr


class AccountSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class AccountPublic(BaseModel):
    id: int
    email: EmailStr
    username: str

    model_config = ConfigDict(from_attributes=True)


class AccountList(BaseModel):
    users: list[AccountPublic]


class MessageSchema(BaseModel):
    message: str
