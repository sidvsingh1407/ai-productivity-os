from datetime import datetime

rev_id = "manual_003"
down_rev = "manual_002"

content = f"""\"\"\"Enable RLS on api_keys and api_usage_logs

Revision ID: {rev_id}
Revises: {down_rev}
Create Date: {datetime.now().isoformat()}

\"\"\"
from typing import Sequence, Union
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '{rev_id}'
down_revision: Union[str, Sequence[str], None] = '{down_rev}'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

tables = [
    'api_keys',
    'api_usage_logs'
]

def upgrade() -> None:
    for table in tables:
        # Enable RLS on the table
        op.execute(f'ALTER TABLE {{table}} ENABLE ROW LEVEL SECURITY;')

        # Create policy denying postgrest access
        op.execute(f'''
            CREATE POLICY "Allow backend access, deny postgrest" ON {{table}}
            AS PERMISSIVE FOR ALL
            USING (current_user NOT IN ('anon', 'authenticated'))
            WITH CHECK (current_user NOT IN ('anon', 'authenticated'));
        ''')


def downgrade() -> None:
    for table in tables:
        # Drop the policy
        op.execute(f'DROP POLICY IF EXISTS "Allow backend access, deny postgrest" ON {{table}};')

        # Disable RLS
        op.execute(f'ALTER TABLE {{table}} DISABLE ROW LEVEL SECURITY;')
"""

with open(f"backend/alembic/versions/{rev_id}_enable_rls_on_api_tables.py", "w") as f:
    f.write(content)

print("Migration file written.")
