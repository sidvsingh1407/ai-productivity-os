"""add_waitlist_extended_fields

Revision ID: 2026_11_05_1443_add_waitlist_extended_fields
Revises: e4e7e0aea591
Create Date: 2026-11-05 14:42:53.698154

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2026_11_05_1443_add_waitlist_extended_fields"
down_revision: Union[str, Sequence[str], None] = 'e4e7e0aea591'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('waitlist_signups', sa.Column('company_size', sa.String(), nullable=True))
    op.add_column('waitlist_signups', sa.Column('problem_statement', sa.String(), nullable=True))
    op.add_column('waitlist_signups', sa.Column('signup_type', sa.String(), server_default='quick', nullable=False))

    op.create_check_constraint(
        'ck_waitlist_signups_signup_type',
        'waitlist_signups',
        "signup_type IN ('quick', 'extended')"
    )

    op.create_index('ix_waitlist_signups_product_preference', 'waitlist_signups', ['product_preference'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_waitlist_signups_product_preference', table_name='waitlist_signups')
    op.drop_constraint('ck_waitlist_signups_signup_type', 'waitlist_signups', type_='check')
    op.drop_column('waitlist_signups', 'signup_type')
    op.drop_column('waitlist_signups', 'problem_statement')
    op.drop_column('waitlist_signups', 'company_size')
