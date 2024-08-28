from typing import Annotated

from pydantic import BaseModel, Field


class NovelistSchema(BaseModel):
    name: Annotated[str, Field(description='name of novelist', max_length=40)]


class NovelistPublic(NovelistSchema):
    id: Annotated[int, Field(description='ID of novelist')]


class NovelistListAll(BaseModel):
    novelists: list[NovelistPublic]


class NovelistUpdate(BaseModel):
    name: str | None = None
