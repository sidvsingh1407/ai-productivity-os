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
        # Enable RLS on the table. RLS enabling is generally safe, but we also revoke all safely.
        op.execute(f'ALTER TABLE public.{table} ENABLE ROW LEVEL SECURITY;')

        op.execute(f'''
            DO $$
            BEGIN
                IF EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'anon') THEN
                    EXECUTE 'REVOKE ALL ON public.{table} FROM anon;';
                END IF;
                IF EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'authenticated') THEN
                    EXECUTE 'REVOKE ALL ON public.{table} FROM authenticated;';
                END IF;
            END
            $$;
        ''')

        # Create policy denying postgrest access if it does not exist
        op.execute(f'''
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM pg_policies
                    WHERE tablename = '{table}' AND policyname = 'Allow backend access, deny postgrest'
                ) THEN
                    CREATE POLICY "Allow backend access, deny postgrest" ON public.{table}
                    AS PERMISSIVE FOR ALL
                    USING (current_user NOT IN ('anon', 'authenticated'))
                    WITH CHECK (current_user NOT IN ('anon', 'authenticated'));
                END IF;
            END
            $$;
        ''')


def downgrade() -> None:
    for table in tables:
        # Drop the policy
        op.execute(f'DROP POLICY IF EXISTS "Allow backend access, deny postgrest" ON public.{table};')

        # Disable RLS
        op.execute(f'ALTER TABLE public.{table} DISABLE ROW LEVEL SECURITY;')
