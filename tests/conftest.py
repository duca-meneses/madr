import pytest
from factory import Factory, LazyAttribute, Sequence
from faker.generator import Generator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer

from madr.app import app
from madr.config.security import get_password_hash
from madr.data.database import get_async_session
from madr.data.models import Account, Book, Novelist, table_registry
from madr.schemas.book import BookPublic
from madr.schemas.novelist import NovelistPublic


class AccountFactory(Factory):
    class Meta:
        model = Account

    username = Sequence(lambda x: f'test{x}')
    email = LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = LazyAttribute(lambda obj: f'{obj.username}@10')


class NovelistFactory(Factory):
    class Meta:
        model = Novelist

    name = Sequence(lambda x: f'test{x}')


class BookFactory(Factory):
    class Meta:
        model = Book

    title = Sequence(lambda x: f'test title {x}')
    year = Sequence(lambda y: f'20{y}')
    author_id = 1


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        # postgres.driver = 'asyncpg'
        yield create_async_engine(postgres.get_connection_url())


@pytest.fixture
async def session(engine: AsyncEngine):
    async with engine.connect() as connection:
        await connection.run_sync(
            lambda con: table_registry.metadata.create_all(con.engine)
        )

        async with AsyncSession(engine, expire_on_commit=False) as session:
            yield session

        await connection.run_sync(
            lambda con: table_registry.metadata.drop_all(con.engine)
        )


@pytest.fixture
async def client(session: AsyncSession):
    async def get_session_override():
        yield session

    app.dependency_overrides[get_async_session] = get_session_override

    async with AsyncClient(app=app, base_url='http://test') as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
async def user(faker: Generator, session: AsyncSession) -> Account:
    password = faker.password()
    new_user = AccountFactory(password=get_password_hash(password))

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    new_user.clean_password = password

    return new_user


@pytest.fixture
async def other_user(faker: Generator, session: AsyncSession):
    pwd = faker.password()
    user = AccountFactory(password=get_password_hash(pwd))

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = pwd  # Monkey patch

    return user


@pytest.fixture
async def token(client: AsyncClient, user: Account):
    response = await client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    return response.json()['access_token']


@pytest.fixture
async def novelist(session: AsyncSession) -> NovelistPublic:
    novelist = NovelistFactory()

    session.add(novelist)
    await session.commit()
    await session.refresh(novelist)

    return novelist


@pytest.fixture
async def other_novelist(session: AsyncSession) -> NovelistPublic:
    novelist = NovelistFactory()

    session.add(novelist)
    await session.commit()
    await session.refresh(novelist)

    return novelist


@pytest.fixture
async def book(session: AsyncSession, novelist: NovelistPublic) -> BookPublic:
    book = BookFactory(author_id=novelist.id)

    session.add(book)
    await session.commit()
    await session.refresh(book)

    return book
