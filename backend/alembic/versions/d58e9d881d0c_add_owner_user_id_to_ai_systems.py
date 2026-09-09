"""add owner_user_id to ai_systems

Revision ID: d58e9d881d0c
Revises: e2bb5eb0e3be
Create Date: 2026-09-06 17:09:09.461865

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd58e9d881d0c'
down_revision: Union[str, Sequence[str], None] = 'e2bb5eb0e3be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('ai_systems', sa.Column('owner_user_id', sa.UUID(), nullable=True))
    op.create_foreign_key('fk_ai_systems_owner_user_id', 'ai_systems', 'users', ['owner_user_id'], ['id'], ondelete='SET NULL')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_ai_systems_owner_user_id', 'ai_systems', type_='foreignkey')
    op.drop_column('ai_systems', 'owner_user_id')
