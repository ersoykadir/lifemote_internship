"""Remove password column from user

Revision ID: e97cee0b8500
Revises: f26a387d5b9c
Create Date: 2023-08-16 15:05:45.851395

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e97cee0b8500'
down_revision: Union[str, None] = 'f26a387d5b9c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("users", "password")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "password",
            sa.VARCHAR(length=255),
            autoincrement=False,
            nullable=False
        )
    )
