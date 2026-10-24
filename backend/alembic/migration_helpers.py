from alembic import op
import sqlalchemy as sa

def table_exists(table_name: str) -> bool:
    bind = op.get_bind()
    insp = sa.inspect(bind)
    return insp.has_table(table_name)

def column_exists(table_name: str, column_name: str) -> bool:
    if not table_exists(table_name):
        return False
    bind = op.get_bind()
    insp = sa.inspect(bind)
    has_column = False
    for c in insp.get_columns(table_name):
        if c['name'] == column_name:
            has_column = True
            break
    return has_column

def index_exists(table_name: str, index_name: str) -> bool:
    if not table_exists(table_name):
        return False
    bind = op.get_bind()
    insp = sa.inspect(bind)
    for i in insp.get_indexes(table_name):
        if i['name'] == index_name:
            return True
    return False

def constraint_exists(table_name: str, constraint_name: str) -> bool:
    if not table_exists(table_name):
        return False
    bind = op.get_bind()
    insp = sa.inspect(bind)

    # Check uniques
    for u in insp.get_unique_constraints(table_name):
        if u['name'] == constraint_name:
            return True

    # Check foreign keys
    for f in insp.get_foreign_keys(table_name):
        if f['name'] == constraint_name:
            return True

    # Check constraints requires dialet specific stuff, but we can do pk
    pk = insp.get_pk_constraint(table_name)
    if pk and pk['name'] == constraint_name:
        return True

    try:
        for c in insp.get_check_constraints(table_name):
            if c['name'] == constraint_name:
                return True
    except NotImplementedError:
        # SQLite doesn't support get_check_constraints via inspector easily
        pass

    return False
