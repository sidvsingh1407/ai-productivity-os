"""add user token and email verification schema

Revision ID: manual_005
Revises: manual_004
Create Date: 2024-06-09 20:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from migration_helpers import table_exists, column_exists, index_exists

# revision identifiers, used by Alembic.
revision: str = 'manual_005'
down_revision: Union[str, None] = 'manual_004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add columns to users table
    if table_exists('users'):
        if not column_exists('users', 'email_verified'):
            op.add_column('users', sa.Column('email_verified', sa.Boolean(), server_default='false', nullable=False))
        if not column_exists('users', 'email_verified_at'):
            op.add_column('users', sa.Column('email_verified_at', sa.DateTime(timezone=True), nullable=True))

    # Create user_tokens table
    if not table_exists('user_tokens'):
        op.create_table('user_tokens',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('token_hash', sa.String(), nullable=False),
        sa.Column('token_type', sa.String(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_user_tokens_token_hash'), 'user_tokens', ['token_hash'], unique=True)
        op.create_index(op.f('ix_user_tokens_user_id'), 'user_tokens', ['user_id'], unique=False)


def downgrade() -> None:
    if table_exists('user_tokens'):
        if index_exists('user_tokens', 'ix_user_tokens_user_id'):
            op.drop_index(op.f('ix_user_tokens_user_id'), table_name='user_tokens')
        if index_exists('user_tokens', 'ix_user_tokens_token_hash'):
            op.drop_index(op.f('ix_user_tokens_token_hash'), table_name='user_tokens')
        op.drop_table('user_tokens')

    if table_exists('users'):
        if column_exists('users', 'email_verified_at'):
            op.drop_column('users', 'email_verified_at')
        if column_exists('users', 'email_verified'):
            op.drop_column('users', 'email_verified')

 main-11068675611994421723
