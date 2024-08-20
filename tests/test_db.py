from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from madr.models import Account


async def test_create_account(session: AsyncSession):
    new_account = Account(
        username='duca_meneses', password='secret', email='duca@test.com'
    )
    session.add(new_account)
    await session.commit()

    account = await session.scalar(
        select(Account).where(Account.username == new_account.username)
    )

    assert account.email == new_account.email
