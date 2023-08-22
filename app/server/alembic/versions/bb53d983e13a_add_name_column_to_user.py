"""Add name column to user

Revision ID: bb53d983e13a
Revises: e97cee0b8500
Create Date: 2023-08-16 15:07:10.343176

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb53d983e13a'
down_revision: Union[str, None] = 'e97cee0b8500'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('name', sa.String(255), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'name')
