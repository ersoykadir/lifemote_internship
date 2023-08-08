"""create item table

Revision ID: c8853462c82a
Revises: 
Create Date: 2023-08-08 14:14:53.447008

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8853462c82a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'item',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('message', sa.String(64), nullable=False),
    )

def downgrade() -> None:
    op.drop_table('item')