"""add_regulation_chunks

Revision ID: ca6463a714d3
Revises: 4314b1ec1b7e
Create Date: 2026-07-20 05:50:03.791748

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = 'ca6463a714d3'
down_revision: Union[str, Sequence[str], None] = '4314b1ec1b7e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create vector extension if on postgres
    bind = op.get_bind()
    if bind.engine.name == 'postgresql':
        op.execute('CREATE EXTENSION IF NOT EXISTS vector')

    op.create_table('regulation_chunks',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('source', sa.String(), nullable=False),
    sa.Column('article_number', sa.String(), nullable=True),
    sa.Column('section_title', sa.String(), nullable=True),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('embedding', Vector(768), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_regulation_chunks_source'), 'regulation_chunks', ['source'], unique=False)

    if bind.engine.name == 'postgresql':
        # Add index for vector similarity search (cosine distance: vector_cosine_ops)
        op.execute("CREATE INDEX ix_regulation_chunks_embedding ON regulation_chunks USING hnsw (embedding vector_cosine_ops)")


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    if bind.engine.name == 'postgresql':
        op.execute("DROP INDEX IF EXISTS ix_regulation_chunks_embedding")
    op.drop_index(op.f('ix_regulation_chunks_source'), table_name='regulation_chunks')
    op.drop_table('regulation_chunks')
