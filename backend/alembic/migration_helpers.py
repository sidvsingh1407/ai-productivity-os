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
    columns = [c["name"] for c in insp.get_columns(table_name)]
    return column_name in columns

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

    for c in insp.get_foreign_keys(table_name):
        if c['name'] == constraint_name:
            return True

    for c in insp.get_unique_constraints(table_name):
        if c['name'] == constraint_name:
            return True

    try:
        for c in insp.get_check_constraints(table_name):
            if c['name'] == constraint_name:
                return True
    except NotImplementedError:
        pass

    return False
