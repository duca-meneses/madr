from typing import Annotated

from pydantic import BaseModel, Field


class BookSchema(BaseModel):
    year: Annotated[str, Field(
        description='year of release', examples=['1899'], max_length=4),
    ]
    title: Annotated[str, Field(
        description='title of book', examples=['Dom Casmurro'], max_length=50),
    ]
    author_id: Annotated[int, Field(description='ID of the novelist')]


class BookPublic(BaseModel):
    id: Annotated[int, Field(
        description='ID of book')
    ]
    year: Annotated[str, Field(
        description='year of release', examples=['1899'], max_length=4),
    ]
    title: Annotated[str, Field(
        description='title of book', examples=['Dom Casmurro'], max_length=50),
    ]
    author_id: Annotated[int, Field(
        description='ID of the novelist')
    ]


class BookList(BaseModel):
    books: list[BookPublic]


class BookUpdate(BaseModel):
    year: str
