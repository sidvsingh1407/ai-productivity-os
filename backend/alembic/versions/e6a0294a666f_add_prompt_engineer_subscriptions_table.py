"""add_prompt_engineer_subscriptions_table

Revision ID: e6a0294a666f
Revises: 0566ff918ed7
Create Date: 2026-07-20 04:46:36.541538

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6a0294a666f'
down_revision: Union[str, Sequence[str], None] = '0566ff918ed7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('prompt_engineer_subscriptions',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('organization_id', sa.Uuid(), nullable=False),
        sa.Column('plan_tier', sa.String(), nullable=False, server_default='unset'),
        sa.Column('status', sa.String(), nullable=False, server_default='inactive'),
        sa.Column('external_subscription_id', sa.String(), nullable=True),
        sa.Column('seat_count', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('billing_cycle', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), onupdate=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_prompt_engineer_subscriptions_organization_id'), 'prompt_engineer_subscriptions', ['organization_id'], unique=False)

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_prompt_engineer_subscriptions_organization_id'), table_name='prompt_engineer_subscriptions')
    op.drop_table('prompt_engineer_subscriptions')
