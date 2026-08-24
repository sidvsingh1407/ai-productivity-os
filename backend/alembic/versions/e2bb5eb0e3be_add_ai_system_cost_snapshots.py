"""add_ai_system_cost_snapshots

Revision ID: e2bb5eb0e3be
Revises: 076f4b8d7aa8
Create Date: 2026-08-24 05:29:05.253749

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e2bb5eb0e3be'
down_revision: Union[str, Sequence[str], None] = '076f4b8d7aa8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'ai_system_cost_snapshots',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('organization_id', sa.Uuid(), nullable=False),
        sa.Column('ai_system_id', sa.Uuid(), nullable=False),
        sa.Column('audit_id', sa.Uuid(), nullable=False),
        sa.Column('licensing_cost', sa.Numeric(), nullable=True),
        sa.Column('cloud_cost', sa.Numeric(), nullable=True),
        sa.Column('inference_cost', sa.Numeric(), nullable=True),
        sa.Column('maintenance_cost', sa.Numeric(), nullable=True),
        sa.Column('total_cost', sa.Numeric(), nullable=True),
        sa.Column('is_partial', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['ai_system_id'], ['ai_systems.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['audit_id'], ['audits.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ai_system_cost_snapshots_ai_system_id'), 'ai_system_cost_snapshots', ['ai_system_id'], unique=False)
    op.create_index(op.f('ix_ai_system_cost_snapshots_audit_id'), 'ai_system_cost_snapshots', ['audit_id'], unique=False)
    op.create_index(op.f('ix_ai_system_cost_snapshots_organization_id'), 'ai_system_cost_snapshots', ['organization_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_ai_system_cost_snapshots_organization_id'), table_name='ai_system_cost_snapshots')
    op.drop_index(op.f('ix_ai_system_cost_snapshots_audit_id'), table_name='ai_system_cost_snapshots')
    op.drop_index(op.f('ix_ai_system_cost_snapshots_ai_system_id'), table_name='ai_system_cost_snapshots')
    op.drop_table('ai_system_cost_snapshots')
