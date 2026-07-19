"""Add data and operations fields to ai_systems

Revision ID: c812aa03f90a
Revises: 4f12c7e5f682
Create Date: 2026-07-19 15:11:39.647729

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import JSON

@compiles(JSONB, "sqlite")
def compile_jsonb_sqlite(type_, compiler, **kw):
    return "JSON"


# revision identifiers, used by Alembic.
revision: str = 'c812aa03f90a'
down_revision: Union[str, Sequence[str], None] = '4f12c7e5f682'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('ai_systems', sa.Column('data_sensitivity', sa.String(), nullable=True))
    op.add_column('ai_systems', sa.Column('data_sources', JSONB, nullable=True))
    op.add_column('ai_systems', sa.Column('data_destinations', JSONB, nullable=True))
    op.add_column('ai_systems', sa.Column('usage_frequency', sa.String(), nullable=True))
    op.add_column('ai_systems', sa.Column('users_count', sa.Integer(), nullable=True))
    op.add_column('ai_systems', sa.Column('uptime', sa.Float(), nullable=True))
    op.add_column('ai_systems', sa.Column('approvals_required', sa.Boolean(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('ai_systems', 'approvals_required')
    op.drop_column('ai_systems', 'uptime')
    op.drop_column('ai_systems', 'users_count')
    op.drop_column('ai_systems', 'usage_frequency')
    op.drop_column('ai_systems', 'data_destinations')
    op.drop_column('ai_systems', 'data_sources')
    op.drop_column('ai_systems', 'data_sensitivity')
