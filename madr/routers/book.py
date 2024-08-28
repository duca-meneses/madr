from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select

from madr.data.models import Book
from madr.schemas.book import BookList, BookPublic, BookSchema, BookUpdate
from madr.schemas.message import MessageSchema
from madr.utils.dependencies import T_CurrentUser, T_Session
from madr.utils.sanitize import sanitize_data

router = APIRouter(prefix='/books', tags=['books'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=BookPublic)
async def create_book(
    book: BookSchema, session: T_Session, user: T_CurrentUser
):
    db_book = await session.scalar(
        select(Book).where(Book.title == book.title)
    )

    if db_book:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='book already on the MADR'
        )

    db_book = Book(
        title=sanitize_data(book.title),
        year=book.year,
        author_id=book.author_id,
    )

    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)

    return db_book


@router.get('/', status_code=HTTPStatus.OK, response_model=BookList)
async def list_books(   # noqa
    session: T_Session,
    user: T_CurrentUser,
    name: str = Query(None),
    year: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(10),
):
    query = select(Book)

    if name:
        query = query.filter(Book.title.contains(name))

    if year:
        query = query.filter(Book.year.contains(year))

    books = await session.scalars(query.offset(offset).limit(limit))

    return {'books': books}


@router.get('/{book_id}', status_code=HTTPStatus.OK, response_model=BookPublic)
async def get_book_by_id(
    book_id: int, session: T_Session, user: T_CurrentUser
):
    db_book = await session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Book not listed in MADR'
        )

    return db_book


@router.patch(
    '/{book_id}', status_code=HTTPStatus.OK, response_model=BookPublic
)
async def update_book(
    book_id: int, booK: BookUpdate, session: T_Session, user: T_CurrentUser
):
    db_book = await session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Book not listed in MADR'
        )

    db_book.year = booK.year

    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)

    return db_book


@router.delete(
    '/{book_id}', status_code=HTTPStatus.OK, response_model=MessageSchema
)
async def delete_book(book_id: int, session: T_Session, user: T_CurrentUser):
    db_book = await session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Book not listed in MADR'
        )

    await session.delete(db_book)
    await session.commit()

    return {'message': 'Book deleted from MADR'}
