"""Add technology fields to ai_systems

Revision ID: 181496e9e133
Revises: 47b16ad19e48
Create Date: 2026-07-19 14:25:42.428980

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '181496e9e133'
down_revision: Union[str, Sequence[str], None] = '47b16ad19e48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # SQLite fallback will happen via sqlalchemy compilation if needed, but in Alembic migrations
    # we typically use sa.JSON to be safe, or postgresql.JSONB if running against Postgres.
    # We will use sa.JSON().with_variant(postgresql.JSONB, 'postgresql') for safety.

    json_type = sa.JSON().with_variant(postgresql.JSONB, 'postgresql')

    op.add_column('ai_systems', sa.Column('vendor', sa.String(), nullable=True))
    op.add_column('ai_systems', sa.Column('model_name', sa.String(), nullable=True))
    op.add_column('ai_systems', sa.Column('model_version', sa.String(), nullable=True))
    op.add_column('ai_systems', sa.Column('api_provider', sa.String(), nullable=True))
    op.add_column('ai_systems', sa.Column('framework', sa.String(), nullable=True))
    op.add_column('ai_systems', sa.Column('hosting', sa.String(), nullable=True))
    op.add_column('ai_systems', sa.Column('integrations', json_type, server_default='[]', nullable=False))
    op.add_column('ai_systems', sa.Column('authentication_method', sa.String(), nullable=True))
    op.add_column('ai_systems', sa.Column('vector_db', sa.String(), nullable=True))
    op.add_column('ai_systems', sa.Column('knowledge_sources', json_type, server_default='[]', nullable=False))
    op.add_column('ai_systems', sa.Column('workflow_engine', sa.String(), nullable=True))
    op.add_column('ai_systems', sa.Column('agent_framework', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('ai_systems', 'agent_framework')
    op.drop_column('ai_systems', 'workflow_engine')
    op.drop_column('ai_systems', 'knowledge_sources')
    op.drop_column('ai_systems', 'vector_db')
    op.drop_column('ai_systems', 'authentication_method')
    op.drop_column('ai_systems', 'integrations')
    op.drop_column('ai_systems', 'hosting')
    op.drop_column('ai_systems', 'framework')
    op.drop_column('ai_systems', 'api_provider')
    op.drop_column('ai_systems', 'model_version')
    op.drop_column('ai_systems', 'model_name')
    op.drop_column('ai_systems', 'vendor')
