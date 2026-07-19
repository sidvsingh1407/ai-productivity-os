"""Add identity business fields ai systems

Revision ID: 47b16ad19e48
Revises: 4c2017c2d049
Create Date: 2026-07-18T18:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47b16ad19e48'
down_revision: Union[str, None] = '4c2017c2d049'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('ai_systems', sa.Column('version', sa.String(), nullable=True))
    op.add_column('ai_systems', sa.Column('lifecycle_status', sa.String(), nullable=True))
    op.add_column('ai_systems', sa.Column('owner', sa.String(), nullable=True))
    op.add_column('ai_systems', sa.Column('department', sa.String(), nullable=True))
    op.add_column('ai_systems', sa.Column('business_capability', sa.String(), nullable=True))
    op.add_column('ai_systems', sa.Column('internal_external_users', sa.String(), nullable=True))
    op.add_column('ai_systems', sa.Column('criticality', sa.String(), nullable=True))
    op.add_column('ai_systems', sa.Column('implementation_stage', sa.String(), nullable=True))
    op.add_column('ai_systems', sa.Column('ai_type', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('ai_systems', 'ai_type')
    op.drop_column('ai_systems', 'implementation_stage')
    op.drop_column('ai_systems', 'criticality')
    op.drop_column('ai_systems', 'internal_external_users')
    op.drop_column('ai_systems', 'business_capability')
    op.drop_column('ai_systems', 'department')
    op.drop_column('ai_systems', 'owner')
    op.drop_column('ai_systems', 'lifecycle_status')
    op.drop_column('ai_systems', 'version')
