"""add_next_run_at_and_monitoring_check_results

Revision ID: 2e9bc28d884d
Revises: 43ab3a4df412
Create Date: 2026-07-21 07:35:37.339261

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e9bc28d884d'
down_revision: Union[str, Sequence[str], None] = '43ab3a4df412'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('monitoring_plans', sa.Column('next_run_at', sa.DateTime(timezone=True), nullable=True))

    op.create_table(
        'monitoring_check_results',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('monitoring_plan_id', sa.UUID(), nullable=False),
        sa.Column('ai_system_id', sa.UUID(), nullable=False),
        sa.Column('findings', sa.dialects.postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('severity', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['ai_system_id'], ['ai_systems.id'], ),
        sa.ForeignKeyConstraint(['monitoring_plan_id'], ['monitoring_plans.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_monitoring_check_results_ai_system_id'), 'monitoring_check_results', ['ai_system_id'], unique=False)
    op.create_index(op.f('ix_monitoring_check_results_monitoring_plan_id'), 'monitoring_check_results', ['monitoring_plan_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_monitoring_check_results_monitoring_plan_id'), table_name='monitoring_check_results')
    op.drop_index(op.f('ix_monitoring_check_results_ai_system_id'), table_name='monitoring_check_results')
    op.drop_table('monitoring_check_results')

    op.drop_column('monitoring_plans', 'next_run_at')
