"""add completed column

Revision ID: 7a977d4d1674
Revises: c8853462c82a
Create Date: 2023-08-08 14:16:01.139714

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import false


# revision identifiers, used by Alembic.
revision: str = '7a977d4d1674'
down_revision: Union[str, None] = 'c8853462c82a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "items", sa.Column("completed", sa.Boolean(), server_default=false())
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("items", "completed")
    # ### end Alembic commands ###
