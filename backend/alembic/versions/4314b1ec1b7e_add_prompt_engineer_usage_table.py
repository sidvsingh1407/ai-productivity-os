"""add_prompt_engineer_usage_table

Revision ID: 4314b1ec1b7e
Revises: e6a0294a666f
Create Date: 2026-07-20 05:16:53.991693

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4314b1ec1b7e'
down_revision: Union[str, Sequence[str], None] = 'e6a0294a666f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('prompt_engineer_usage',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('subscription_id', sa.Uuid(), nullable=False),
        sa.Column('organization_id', sa.Uuid(), nullable=False),
        sa.Column('usage_type', sa.String(), nullable=False),
        sa.Column('token_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('request_count', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('model_used', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.ForeignKeyConstraint(['subscription_id'], ['prompt_engineer_subscriptions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_prompt_engineer_usage_organization_id'), 'prompt_engineer_usage', ['organization_id'], unique=False)
    op.create_index(op.f('ix_prompt_engineer_usage_subscription_id'), 'prompt_engineer_usage', ['subscription_id'], unique=False)

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_prompt_engineer_usage_subscription_id'), table_name='prompt_engineer_usage')
    op.drop_index(op.f('ix_prompt_engineer_usage_organization_id'), table_name='prompt_engineer_usage')
    op.drop_table('prompt_engineer_usage')
