from http import HTTPStatus

from httpx import AsyncClient


async def test_read_root(client: AsyncClient):
    response = await client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'server': 'up'}
