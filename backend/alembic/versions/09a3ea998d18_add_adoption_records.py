"""add_adoption_records

Revision ID: 09a3ea998d18
Revises: 2e9bc28d884d
Create Date: 2026-07-21 10:44:41.834199

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '09a3ea998d18'
down_revision: Union[str, Sequence[str], None] = '2e9bc28d884d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'adoption_records',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('organization_id', sa.Uuid(), nullable=False),
        sa.Column('ai_system_id', sa.Uuid(), nullable=False),
        sa.Column('department', sa.String(), nullable=False),
        sa.Column('user_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('usage_frequency', sa.String(), server_default='not_specified', nullable=False),
        sa.Column('shadow_ai_detected', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('champions', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'"), nullable=False),
        sa.Column('resistance_level', sa.String(), server_default='not_specified', nullable=False),
        sa.Column('training_status', sa.String(), server_default='not_specified', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.ForeignKeyConstraint(['ai_system_id'], ['ai_systems.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ai_system_id', 'department', name='uix_ai_system_department')
    )
    op.create_index(op.f('ix_adoption_records_organization_id'), 'adoption_records', ['organization_id'], unique=False)
    op.create_index(op.f('ix_adoption_records_ai_system_id'), 'adoption_records', ['ai_system_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_adoption_records_ai_system_id'), table_name='adoption_records')
    op.drop_index(op.f('ix_adoption_records_organization_id'), table_name='adoption_records')
    op.drop_table('adoption_records')
