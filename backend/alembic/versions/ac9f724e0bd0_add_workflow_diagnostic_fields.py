"""add_workflow_diagnostic_fields

Revision ID: ac9f724e0bd0
Revises: 09a3ea998d18
Create Date: 2026-07-22 15:39:47.729414

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac9f724e0bd0'
down_revision: Union[str, Sequence[str], None] = '09a3ea998d18'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from sqlalchemy.dialects import postgresql

def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('workflows', sa.Column('steps_input', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('workflows', sa.Column('scores', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('workflows', sa.Column('findings', postgresql.JSONB(astext_type=sa.Text()), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('workflows', 'findings')
    op.drop_column('workflows', 'scores')
    op.drop_column('workflows', 'steps_input')
