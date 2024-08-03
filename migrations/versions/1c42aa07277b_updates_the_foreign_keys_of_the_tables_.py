"""updates the foreign keys of the tables  and add column created_at

Revision ID: 1c42aa07277b
Revises: c41190d4866b
Create Date: 2024-08-03 18:47:39.072134

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c42aa07277b'
down_revision: Union[str, None] = 'c41190d4866b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('accounts', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('books', sa.Column('author_id', sa.Integer(), nullable=False))
    op.add_column('books', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.create_foreign_key(None, 'books', 'novelists', ['author_id'], ['id'])
    op.add_column('novelists', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('novelists', 'created_at')
    op.drop_constraint(None, 'books', type_='foreignkey')
    op.drop_column('books', 'created_at')
    op.drop_column('books', 'author_id')
    op.drop_column('accounts', 'created_at')
    # ### end Alembic commands ###
