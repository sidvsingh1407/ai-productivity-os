"""add architecture fields to ai_systems

Revision ID: 4f12c7e5f682
Revises: 181496e9e133
Create Date: 2026-07-19 14:37:33.790202

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# import the same decorator logic that models/ai_system.py uses for sqlite JSONB compilation
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import JSON

@compiles(JSONB, "sqlite")
def compile_jsonb_sqlite(type_, compiler, **kw):
    return "JSON"


# revision identifiers, used by Alembic.
revision: str = '4f12c7e5f682'
down_revision: Union[str, Sequence[str], None] = '181496e9e133'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('ai_systems', sa.Column('deployment_type', sa.String(), nullable=True))
    op.add_column('ai_systems', sa.Column('data_flow', sa.Text(), nullable=True))
    op.add_column('ai_systems', sa.Column('apis', JSONB, nullable=True))
    op.add_column('ai_systems', sa.Column('databases', JSONB, nullable=True))
    op.add_column('ai_systems', sa.Column('event_systems', sa.Text(), nullable=True))
    op.add_column('ai_systems', sa.Column('caching', sa.Text(), nullable=True))
    op.add_column('ai_systems', sa.Column('monitoring', sa.Text(), nullable=True))
    op.add_column('ai_systems', sa.Column('logging', sa.Text(), nullable=True))
    op.add_column('ai_systems', sa.Column('deployment_details', sa.Text(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('ai_systems', 'deployment_details')
    op.drop_column('ai_systems', 'logging')
    op.drop_column('ai_systems', 'monitoring')
    op.drop_column('ai_systems', 'caching')
    op.drop_column('ai_systems', 'event_systems')
    op.drop_column('ai_systems', 'databases')
    op.drop_column('ai_systems', 'apis')
    op.drop_column('ai_systems', 'data_flow')
    op.drop_column('ai_systems', 'deployment_type')
