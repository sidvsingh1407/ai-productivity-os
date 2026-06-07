"""Add system deleted user

Revision ID: manual_002
Revises: a1b2c3d4e5f6
Create Date: 2024-06-07 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'manual_002'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # We create a specific UUID for the deleted user so it's consistent and can be referenced
    # Or we can insert it if it doesn't exist
    op.execute("""
        INSERT INTO users (id, email, hashed_password, full_name, is_superadmin, is_active, created_at, updated_at)
        VALUES ('00000000-0000-0000-0000-000000000000', 'deleted@system.tarkax.local', '', 'Deleted User', false, false, NOW(), NOW())
        ON CONFLICT (email) DO NOTHING;
    """)


def downgrade() -> None:
    op.execute("DELETE FROM users WHERE email = 'deleted@system.tarkax.local'")
