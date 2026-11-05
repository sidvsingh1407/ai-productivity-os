"""add waitlist_signups table

Revision ID: e4e7e0aea591
Revises: 89ef21c9d6a4
Create Date: 2026-11-05 09:37:03.506901

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4e7e0aea591'
down_revision: Union[str, Sequence[str], None] = '89ef21c9d6a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'waitlist_signups',
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('product_preference', sa.String(), nullable=True),
        sa.Column('source', sa.String(), nullable=False),
        sa.Column('ip_hash', sa.String(), nullable=False),
        sa.Column('confirmed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('confirmation_token', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('confirmation_token')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('waitlist_signups')
