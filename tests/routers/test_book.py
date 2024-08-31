from http import HTTPStatus

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from madr.schemas.book import BookPublic
from madr.schemas.novelist import NovelistPublic
from tests.conftest import BookFactory


async def test_create_book_with_return_created(
    client: AsyncClient, token: str, novelist: NovelistPublic
):
    response = await client.post(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'O Hobbit',
            'year': '1937',
            'author_id': novelist.id,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'title': 'o hobbit',
        'year': '1937',
        'author_id': novelist.id,
    }


async def test_create_book_with_return_unprocessable_entity(
    client: AsyncClient, token: str, novelist: NovelistPublic
):
    response = await client.post(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'New Book', 'year': 'asdf', 'author_id': novelist.id},
    )
    error_response_msg = response.json()['detail'][0]['msg']

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert error_response_msg == 'Value error, Invalid year format'


async def test_create_book_with_return_conflict(
    client: AsyncClient, token: str, novelist: NovelistPublic, book: BookPublic
):
    response = await client.post(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': book.title, 'year': '2018', 'author_id': novelist.id},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'book already on the MADR'}


async def test_list_books_with_return_empty_list(
    client: AsyncClient,
    token: str,
):
    response = await client.get(
        '/books/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'books': []}


async def test_list_books_with_return_5_books(
    client: AsyncClient,
    token: str,
    session: AsyncSession,
    novelist: NovelistPublic,
):
    expected_books = 5

    await session.run_sync(
        lambda n: n.bulk_save_objects(
            BookFactory.create_batch(5, author_id=novelist.id)
        )
    )
    await session.commit()

    response = await client.get(
        '/books/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['books']) == expected_books


async def test_list_books_pagination_should_return_2(
    client: AsyncClient,
    token: str,
    session: AsyncSession,
    novelist: NovelistPublic,
):
    expected_books = 2

    await session.run_sync(
        lambda n: n.bulk_save_objects(
            BookFactory.create_batch(5, author_id=novelist.id)
        )
    )
    await session.commit()

    response = await client.get(
        '/books/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['books']) == expected_books


async def test_list_books_filter_title_should_return_5(
    client: AsyncClient,
    token: str,
    session: AsyncSession,
    novelist: NovelistPublic,
):
    expected_books = 5

    await session.run_sync(
        lambda n: n.bulk_save_objects(
            BookFactory.create_batch(5, author_id=novelist.id)
        )
    )
    await session.commit()

    response = await client.get(
        '/books/?title=ti', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['books']) == expected_books


async def test_list_books_filter_year_should_return_1(
    client: AsyncClient,
    token: str,
    session: AsyncSession,
    novelist: NovelistPublic,
):
    expected_books = 5

    await session.run_sync(
        lambda n: n.bulk_save_objects(
            BookFactory.create_batch(5, author_id=novelist.id)
        )
    )
    await session.commit()

    response = await client.get(
        '/books/?year=20', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['books']) == expected_books


async def test_get_books_by_id_with_return_ok(
    client: AsyncClient,
    token: str,
    book: BookPublic,
):
    response = await client.get(
        f'/books/{book.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': book.id,
        'title': book.title,
        'year': book.year,
        'author_id': book.author_id,
    }


async def test_get_books_by_id_with_return_not_found(
    client: AsyncClient,
    token: str,
    book: BookPublic,
):
    response = await client.get(
        '/books/10', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not listed in MADR'}


async def test_update_book_with_return_ok(
    client: AsyncClient, token: str, book: BookPublic
):
    new_year = '2024'

    response = await client.patch(
        f'/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'year': new_year},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['year'] == new_year


async def test_update_book_with_return_unprocessable_entity(
    client: AsyncClient, token: str, book: BookPublic
):
    new_year = 'asd4'

    response = await client.patch(
        f'/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'year': new_year},
    )

    error_response_msg = response.json()['detail'][0]['msg']

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert error_response_msg == response.json()['detail'][0]['msg']


async def test_update_book_with_return_not_found(
    client: AsyncClient, token: str, book: BookPublic
):
    response = await client.patch(
        '/books/2',
        headers={'Authorization': f'Bearer {token}'},
        json={'year': '2023'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not listed in MADR'}


async def test_delete_book_with_return_ok(
    client: AsyncClient, token: str, book: BookPublic
):
    response = await client.delete(
        f'/books/{book.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Book deleted from MADR'}


async def test_delete_book_with_return_not_found(
    client: AsyncClient, token: str, book: BookPublic
):
    response = await client.delete(
        '/books/2', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not listed in MADR'}
