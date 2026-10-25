"""Enable RLS on all tables

Revision ID: 89ef21c9d6a4
Revises: a4da25a47216
Create Date: 2024-11-20 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = '89ef21c9d6a4'
down_revision: Union[str, Sequence[str], None] = 'a4da25a47216'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = inspect(conn)
    tables = inspector.get_table_names()

    for table in tables:
        # Ignore alembic_version table
        if table == 'alembic_version':
            continue

        # Enable RLS on the table
        op.execute(f'ALTER TABLE public."{table}" ENABLE ROW LEVEL SECURITY;')

        op.execute(f'''
            DO $$
            BEGIN
                IF EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'anon') THEN
                    EXECUTE 'REVOKE ALL ON public."{table}" FROM anon;';
                END IF;
                IF EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'authenticated') THEN
                    EXECUTE 'REVOKE ALL ON public."{table}" FROM authenticated;';
                END IF;
            END
            $$;
        ''')


def downgrade() -> None:
    conn = op.get_bind()
    inspector = inspect(conn)
    tables = inspector.get_table_names()

    for table in tables:
        if table == 'alembic_version':
            continue

        # Disable RLS
        op.execute(f'ALTER TABLE public."{table}" DISABLE ROW LEVEL SECURITY;')
