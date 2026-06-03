"""Enable RLS and restrict PostgREST

Revision ID: 7a8b9c0d1e2f
Revises: 6f5a34a2e5d9
Create Date: 2026-05-18 07:00:00.000000

"""
from typing import Sequence, Union
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '7a8b9c0d1e2f'
down_revision: Union[str, Sequence[str], None] = '6f5a34a2e5d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

tables = [
    'users',
    'organizations',
    'org_members',
    'audits',
    'workflows',
    'reports',
    'export_jobs',
    'subscriptions',
    'invitations',
    'audit_versions',
    'blueprints',
    'integration_results',
    'billing_plans'
]

def upgrade() -> None:
    for table in tables:
        # Enable RLS on the table
        op.execute(f'ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;')

        # Create a policy that allows access to all roles EXCEPT the Supabase PostgREST default public roles ('anon', 'authenticated').
        # This allows the backend connection (e.g. 'postgres' or a custom service role) to function normally,
        # while denying direct API queries via Supabase APIs.
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
