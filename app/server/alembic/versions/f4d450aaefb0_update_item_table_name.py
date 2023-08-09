"""update item table name

Revision ID: f4d450aaefb0
Revises: 7a977d4d1674
Create Date: 2023-08-08 16:09:36.835913

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4d450aaefb0'
down_revision: Union[str, None] = '7a977d4d1674'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index(op.f('ix_item_message'), table_name='item')
    op.drop_index(op.f('ix_item_id'), table_name='item')
    op.rename_table('item', 'items')
    op.create_index(op.f('ix_items_id'), 'items', ['id'], unique=False)
    op.create_index(op.f('ix_items_message'), 'items', ['message'], unique=False)
   
def downgrade() -> None:
    op.drop_index(op.f('ix_items_message'), table_name='items')
    op.drop_index(op.f('ix_items_id'), table_name='items')
    op.rename_table('items', 'item')
    op.create_index(op.f('ix_item_id'), 'item', ['id'], unique=False)
    op.create_index(op.f('ix_item_message'), 'item', ['message'], unique=False)