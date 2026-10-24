"""add owner_user_id to ai_systems

Revision ID: d58e9d881d0c
Revises: e2bb5eb0e3be
Create Date: 2026-09-06 17:09:09.461865

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from migration_helpers import column_exists, constraint_exists

# revision identifiers, used by Alembic.
revision: str = 'd58e9d881d0c'
down_revision: Union[str, Sequence[str], None] = 'e2bb5eb0e3be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    if not column_exists('ai_systems', 'owner_user_id'):
        op.add_column('ai_systems', sa.Column('owner_user_id', sa.UUID(), nullable=True))
    if not constraint_exists('ai_systems', 'fk_ai_systems_owner_user_id'):
        op.create_foreign_key('fk_ai_systems_owner_user_id', 'ai_systems', 'users', ['owner_user_id'], ['id'], ondelete='SET NULL')


def downgrade() -> None:
    """Downgrade schema."""
    if constraint_exists('ai_systems', 'fk_ai_systems_owner_user_id'):
        op.drop_constraint('fk_ai_systems_owner_user_id', 'ai_systems', type_='foreignkey')
    if column_exists('ai_systems', 'owner_user_id'):
        op.drop_column('ai_systems', 'owner_user_id')
