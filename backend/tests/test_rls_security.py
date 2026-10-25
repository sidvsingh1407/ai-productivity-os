import pytest
from sqlalchemy import text
from database import engine

@pytest.mark.asyncio
async def test_rls_enabled_on_all_public_tables():
    if engine.name == "sqlite":
        pytest.skip("RLS tests require PostgreSQL. Skipping on SQLite.")

    async with engine.connect() as conn:
        # Get all public tables except alembic_version
        result = await conn.execute(text('''
            SELECT tablename
            FROM pg_tables
            WHERE schemaname = 'public' AND tablename != 'alembic_version';
        '''))
        tables = [row[0] for row in result.all()]

        for table in tables:
            # Check if RLS is enabled
            rls_check = await conn.execute(text(f'''
                SELECT relrowsecurity
                FROM pg_class
                WHERE relname = '{table}' AND relnamespace = (
                    SELECT oid FROM pg_namespace WHERE nspname = 'public'
                );
            '''))
            is_rls_enabled = rls_check.scalar()
            assert is_rls_enabled is True, f"RLS is not enabled on table: {table}"

            # Check permissions for 'anon' and 'authenticated' if roles exist
            for role in ['anon', 'authenticated']:
                role_check = await conn.execute(text(f"SELECT 1 FROM pg_roles WHERE rolname = '{role}'"))
                if role_check.scalar():
                    privs_check = await conn.execute(text(f'''
                        SELECT has_table_privilege('{role}', 'public."{table}"', 'SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER');
                    '''))
                    # We expect has_table_privilege to raise an error if revoked or return False
                    has_privs = privs_check.scalar()
                    assert not has_privs, f"Role {role} has privileges on {table}"
