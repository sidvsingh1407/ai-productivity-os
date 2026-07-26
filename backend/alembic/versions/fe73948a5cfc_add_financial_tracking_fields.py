"""add_financial_tracking_fields

Revision ID: fe73948a5cfc
Revises: 38497379cfb6
Create Date: 2026-07-26 04:14:59.555188

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe73948a5cfc'
down_revision: Union[str, Sequence[str], None] = '38497379cfb6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('ai_systems', sa.Column('licensing_cost', sa.Numeric(), nullable=True))
    op.add_column('ai_systems', sa.Column('cloud_cost', sa.Numeric(), nullable=True))
    op.add_column('ai_systems', sa.Column('inference_cost', sa.Numeric(), nullable=True))
    op.add_column('ai_systems', sa.Column('maintenance_cost', sa.Numeric(), nullable=True))
    op.add_column('ai_systems', sa.Column('cost_currency', sa.String(), nullable=True, server_default='USD'))
    op.add_column('ai_systems', sa.Column('expected_benefits', sa.Text(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('ai_systems', 'expected_benefits')
    op.drop_column('ai_systems', 'cost_currency')
    op.drop_column('ai_systems', 'maintenance_cost')
    op.drop_column('ai_systems', 'inference_cost')
    op.drop_column('ai_systems', 'cloud_cost')
    op.drop_column('ai_systems', 'licensing_cost')
