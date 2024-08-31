from typing import Annotated, Optional

from pydantic import BaseModel, Field, field_validator

MIN_YEAR = 900
MAX_YEAR = 2099


class BookSchema(BaseModel):
    year: Annotated[
        str,
        Field(
            description='year of release',
            examples=['1899'],
            max_length=4,
            min_length=3,
        ),
    ]
    title: Annotated[
        str,
        Field(
            description='title of book',
            examples=['Dom Casmurro'],
            max_length=50,
        ),
    ]
    author_id: Annotated[int, Field(description='ID of the novelist')]

    @field_validator('year')
    @classmethod
    def _year_validate(cls, year: str) -> str:
        try:
            year_int = int(year)
            if MIN_YEAR <= year_int <= MAX_YEAR:
                return year

        except ValueError:
            raise ValueError('Invalid year format')


class BookPublic(BookSchema):
    id: Annotated[int, Field(description='ID of book')]


class BookList(BaseModel):
    books: list[BookPublic]


class BookUpdate(BaseModel):
    year: Annotated[
        Optional[str],
        Field(
            description='year of release',
            examples=['1899'],
            max_length=4,
            min_length=3,
        ),
    ]

    @field_validator('year')
    @classmethod
    def _year_validate(cls, year: str) -> str:
        try:
            year_int = int(year)
            if MIN_YEAR <= year_int <= MAX_YEAR:
                return year
        except ValueError:
            raise ValueError('Invalid year format')
