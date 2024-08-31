from http import HTTPStatus

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from madr.schemas.novelist import NovelistPublic
from tests.conftest import NovelistFactory


async def test_create_novelist_with_return_created(client: AsyncClient, token):
    response = await client.post(
        '/novelist/',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'J. R. R. Tolkien'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, 'name': 'j. r. r. tolkien'}


async def test_create_novelist_with_return_conflict(
    client: AsyncClient, novelist: NovelistPublic, token: str
):
    response = await client.post(
        '/novelist/',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': novelist.name},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'novelist already on the MADR'}


async def test_list_novelist_with_return_empty_list(
    client: AsyncClient, token: str
):
    response = await client.get(
        '/novelist/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'novelists': []}


async def test_list_novelist_with_return_5_novelist(
    client: AsyncClient, session: AsyncSession, token: str
):
    expected_novelists = 5

    await session.run_sync(
        lambda n: n.bulk_save_objects(NovelistFactory.create_batch(5))
    )
    await session.commit()

    response = await client.get(
        '/novelist/', headers={'Authorization': f'Bearer {token}'}
    )

    assert len(response.json()['novelists']) == expected_novelists


async def test_novelist_pagination_should_return_2(
    client: AsyncClient, session: AsyncSession, token: str
):
    expected_novelists = 2

    await session.run_sync(
        lambda n: n.bulk_save_objects(NovelistFactory.create_batch(5))
    )
    await session.commit()

    response = await client.get(
        '/novelist/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['novelists']) == expected_novelists


async def test_novelists_filter_name_should_return_5_novelists(
    client: AsyncClient, session: AsyncSession, token: str
):
    expected_novelists = 5

    await session.run_sync(
        lambda n: n.bulk_save_objects(NovelistFactory.create_batch(5))
    )
    await session.commit()

    response = await client.get(
        '/novelist/?name=tes', headers={'Authorization': f'Bearer {token}'}
    )

    assert len(response.json()['novelists']) == expected_novelists


async def test_get_novelist_by_id_ok(
    client: AsyncClient, token: str, novelist: NovelistPublic
):
    response = await client.get(
        f'/novelist/{novelist.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'name': novelist.name, 'id': novelist.id}


async def test_get_novelist_by_id_not_found(client: AsyncClient, token: str):
    response = await client.get(
        '/novelist/999', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert 'Novelist not listed in MADR' in response.text


async def test_update_novelist_ok(
    client: AsyncClient, token: str, novelist: NovelistPublic
):
    new_name = 'Updated Novelist Name'
    response = await client.patch(
        f'/novelist/{novelist.id}',
        json={'name': new_name},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['name'] == new_name.lower()


async def test_update_novelist_not_found(client: AsyncClient, token: str):
    response = await client.patch(
        '/novelist/999',
        json={'name': 'Updated Novelist Name'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert 'Novelist not listed in MADR' in response.text


async def test_update_novelist_return_conflict(
    client: AsyncClient,
    token: str,
    novelist: NovelistPublic,
    other_novelist: NovelistPublic,
):
    response = await client.patch(
        f'/novelist/{other_novelist.id}',
        json={'name': novelist.name},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'novelist already on the MADR'}


async def test_delete_novelist_with_return_ok(
    client: AsyncClient, token: str, novelist: NovelistPublic
):
    response = await client.delete(
        f'/novelist/{novelist.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Novelist deleted from MADR'}


async def test_delete_novelist_with_return_not_found(
    client: AsyncClient, token: str, novelist: NovelistPublic
):
    response = await client.delete(
        '/novelist/2', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Novelist not listed in MADR'}
