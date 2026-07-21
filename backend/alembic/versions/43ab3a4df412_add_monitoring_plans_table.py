"""add_monitoring_plans_table

Revision ID: 43ab3a4df412
Revises: c7b4b8d46cba
Create Date: 2026-07-21 07:00:55.649320

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43ab3a4df412'
down_revision: Union[str, Sequence[str], None] = 'c7b4b8d46cba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'monitoring_plans',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('ai_system_id', sa.UUID(), nullable=False),
        sa.Column('risk_classification_id', sa.UUID(), nullable=True),
        sa.Column('status', sa.String(), nullable=False, server_default='draft'),
        sa.Column('monitoring_scope', sa.dialects.postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('review_cadence', sa.String(), nullable=True),
        sa.Column('last_reviewed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['ai_system_id'], ['ai_systems.id'], ),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.ForeignKeyConstraint(['risk_classification_id'], ['risk_classifications.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_monitoring_plans_ai_system_id'), 'monitoring_plans', ['ai_system_id'], unique=False)
    op.create_index(op.f('ix_monitoring_plans_organization_id'), 'monitoring_plans', ['organization_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_monitoring_plans_organization_id'), table_name='monitoring_plans')
    op.drop_index(op.f('ix_monitoring_plans_ai_system_id'), table_name='monitoring_plans')
    op.drop_table('monitoring_plans')
