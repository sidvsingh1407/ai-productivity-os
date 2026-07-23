"""add_engineering_records

Revision ID: b7f21d169746
Revises: 09a3ea998d18
Create Date: 2026-07-21 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'b7f21d169746'
down_revision: Union[str, Sequence[str], None] = '09a3ea998d18'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'engineering_records',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('organization_id', sa.Uuid(), nullable=False),

        sa.Column('has_dedicated_ai_team', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('team_size', sa.Integer(), server_default='0', nullable=False),
        sa.Column('roles', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'"), nullable=False),

        sa.Column('consultants_used', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'"), nullable=False),

        sa.Column('has_mlops_pipeline', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('monitoring_tooling', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'"), nullable=False),

        sa.Column('has_dedicated_prompt_engineer', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('prompt_engineer_count', sa.Integer(), server_default='0', nullable=False),

        sa.Column('has_dedicated_devops', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('devops_support_type', sa.String(), server_default='not_specified', nullable=False),

        sa.Column('ai_engineering_budget', sa.Numeric(), nullable=True),
        sa.Column('planned_investment_roadmap', sa.Text(), nullable=True),

        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),

        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('organization_id', name='uix_org_engineering_record')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('engineering_records')
