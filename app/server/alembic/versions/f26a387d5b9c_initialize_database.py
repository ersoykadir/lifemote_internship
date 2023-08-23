"""initialize database

Revision ID: f26a387d5b9c
Revises: c1c8aa86eeec
Create Date: 2023-08-10 13:54:19.233129

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f26a387d5b9c'
down_revision: Union[str, None] = 'c1c8aa86eeec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE users AUTO_INCREMENT = 1;")
    op.execute("INSERT INTO users (email, password) VALUES ('admin', 'admin');")
    
    op.execute("ALTER TABLE contexts AUTO_INCREMENT = 1;")
    op.execute("""  INSERT INTO contexts (name, description, owner_id)
                    VALUES ('To-Do', 'Default To-Do context', 1);""")
    op.execute("""  INSERT INTO contexts (name, description, owner_id)
                    VALUES ('In-Progress', 'Default In-Progress context', 1);""")
    op.execute("""  INSERT INTO contexts (name, description, owner_id)
                    VALUES ('Done', 'Default Done context', 1);""")

def downgrade() -> None:
    op.execute("""  DELETE FROM contexts
                    WHERE name = 'To-Do';""")
    op.execute("""  DELETE FROM contexts
                    WHERE name = 'In-Progress';""")
    op.execute("""  DELETE FROM contexts
                    WHERE name = 'Done';""")
    op.execute("""  DELETE FROM users
                    WHERE email = 'admin';""")