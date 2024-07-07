from sqlalchemy import select

from madr.models import Account


def test_create_account(session):
    new_account = Account(
        username='duca_meneses', password='secret', email='duca@test.com'
    )
    session.add(new_account)
    session.commit()

    account = session.scalar(
        select(Account).where(Account.username == new_account.username)
    )

    assert account.email == new_account.email
