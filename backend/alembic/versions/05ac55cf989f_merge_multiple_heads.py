"""Merge multiple heads

Revision ID: 05ac55cf989f
Revises: 8d9e0f1g2h3i, 9f8e7d6c5b4a
Create Date: 2026-06-06 21:00:46.688293

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05ac55cf989f'
down_revision: Union[str, Sequence[str], None] = ('8d9e0f1g2h3i', '9f8e7d6c5b4a')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
