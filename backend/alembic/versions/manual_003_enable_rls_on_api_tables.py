"""Enable RLS on api_keys and api_usage_logs

Revision ID: manual_003
Revises: manual_002
Create Date: 2026-06-08T09:52:16.275448

"""
from typing import Sequence, Union
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'manual_003'
down_revision: Union[str, Sequence[str], None] = 'manual_002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

tables = [
    'api_keys',
    'api_usage_logs'
]

def upgrade() -> None:
    for table in tables:
        # Enable RLS on the table
        op.execute(f'ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;')

        # Create policy denying postgrest access
        op.execute(f'''
            CREATE POLICY "Allow backend access, deny postgrest" ON {table}
            AS PERMISSIVE FOR ALL
            USING (current_user NOT IN ('anon', 'authenticated'))
            WITH CHECK (current_user NOT IN ('anon', 'authenticated'));
        ''')


def downgrade() -> None:
    for table in tables:
        # Drop the policy
        op.execute(f'DROP POLICY IF EXISTS "Allow backend access, deny postgrest" ON {table};')

        # Disable RLS
        op.execute(f'ALTER TABLE {table} DISABLE ROW LEVEL SECURITY;')
