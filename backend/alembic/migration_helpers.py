from alembic import op
import sqlalchemy as sa

# Merge-safe migration helpers used by idempotent Alembic revisions.
# These checks prevent rerunning migrations from failing when tables,
# columns, indexes, or constraints already exist on the target database.
def table_exists(table_name: str) -> bool:
    bind = op.get_bind()
    if bind is None:
        return False
    insp = sa.inspect(bind)
    return insp.has_table(table_name)


def column_exists(table_name: str, column_name: str) -> bool:
    if not table_exists(table_name):
        return False
    bind = op.get_bind()
    if bind is None:
        return False
    insp = sa.inspect(bind)
    for c in insp.get_columns(table_name):
        if c['name'] == column_name:
            return True
    return False


def index_exists(table_name: str, index_name: str) -> bool:
    if not table_exists(table_name):
        return False
    bind = op.get_bind()
    if bind is None:
        return False
    insp = sa.inspect(bind)
    for i in insp.get_indexes(table_name):
        if i['name'] == index_name:
            return True
    return False


def constraint_exists(table_name: str, constraint_name: str) -> bool:
    if not table_exists(table_name):
        return False
    bind = op.get_bind()
    if bind is None:
        return False
    insp = sa.inspect(bind)

    for u in insp.get_unique_constraints(table_name):
        if u.get('name') == constraint_name:
            return True

    for f in insp.get_foreign_keys(table_name):
        if f.get('name') == constraint_name:
            return True

    pk = insp.get_pk_constraint(table_name)
    if pk and pk.get('name') == constraint_name:
        return True

    try:
        for c in insp.get_check_constraints(table_name):
            if c.get('name') == constraint_name:
                return True
    except (NotImplementedError, AttributeError):
        pass

    return False
