"""merge_heads

Revision ID: 38497379cfb6
Revises: b7f21d169746, c4d8881917c3
Create Date: 2026-07-26 04:14:34.902571

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38497379cfb6'
down_revision: Union[str, Sequence[str], None] = ('b7f21d169746', 'c4d8881917c3')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
