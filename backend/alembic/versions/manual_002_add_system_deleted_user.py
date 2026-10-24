"""Add system deleted user

Revision ID: manual_002
Revises: a1b2c3d4e5f6
Create Date: 2024-06-07 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from migration_helpers import table_exists

# revision identifiers, used by Alembic.
revision: str = 'manual_002'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    if table_exists('users'):
        op.execute("""
            INSERT INTO users (id, email, hashed_password, full_name, is_superadmin, is_active, created_at, updated_at)
            VALUES ('00000000-0000-0000-0000-000000000000', 'deleted@system.tarkax.local', '', 'Deleted User', false, false, NOW(), NOW())
            ON CONFLICT (email) DO NOTHING;
        """)


def downgrade() -> None:
    if table_exists('users'):
        op.execute("""
            DO $$
            DECLARE
                system_user_id UUID;
            BEGIN
                SELECT id INTO system_user_id FROM users WHERE email = 'deleted@system.tarkax.local';

                IF system_user_id IS NOT NULL THEN
                    IF NOT EXISTS (SELECT 1 FROM ai_systems WHERE owner_user_id = system_user_id) AND
                       NOT EXISTS (SELECT 1 FROM user_tokens WHERE user_id = system_user_id) AND
                       NOT EXISTS (SELECT 1 FROM api_keys WHERE user_id = system_user_id) THEN
                        DELETE FROM users WHERE id = system_user_id;
                    END IF;
                END IF;
            END $$;
        """)
