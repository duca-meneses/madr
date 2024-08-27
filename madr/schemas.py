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


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class NovelistSchema(BaseModel):
    name: str


class NovelistPublic(BaseModel):
    id: int
    name: str


class NovelistListAll(BaseModel):
    novelists: list[NovelistPublic]


class NovelistUpdate(BaseModel):
    name: str | None = None
