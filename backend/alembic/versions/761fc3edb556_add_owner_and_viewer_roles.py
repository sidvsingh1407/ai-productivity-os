"""Add owner and viewer roles

Revision ID: 761fc3edb556
Revises: 7a8b9c0d1e2f
Create Date: 2026-06-05 20:54:07.346333

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '761fc3edb556'
down_revision: Union[str, Sequence[str], None] = '7a8b9c0d1e2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # We are using PostgreSQL ENUM. To add values safely without breaking existing data:
    # Note: SQLite does not support ALTER TYPE, so this migration is specifically for PostgreSQL.
    op.execute("ALTER TYPE orgrole ADD VALUE IF NOT EXISTS 'owner'")
    op.execute("ALTER TYPE orgrole ADD VALUE IF NOT EXISTS 'viewer'")

def downgrade() -> None:
    """Downgrade schema."""
    # Removing enum values in postgres is complicated. It usually requires creating a new type,
    # converting the column to the new type, and dropping the old type.
    # For a safe rollback we'll just ignore the downgrade for now.
    pass
