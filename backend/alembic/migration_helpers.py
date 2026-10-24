from alembic import op
import sqlalchemy as sa

 main-11068675611994421723
def column_exists(table_name: str, column_name: str) -> bool:
    if not table_exists(table_name):
        return False
    bind = op.get_bind()
 main-11068675611994421723

def index_exists(table_name: str, index_name: str) -> bool:
    if not table_exists(table_name):
        return False
    bind = op.get_bind()
 main-11068675611994421723
    insp = sa.inspect(bind)
    for i in insp.get_indexes(table_name):
        if i['name'] == index_name:
            return True
    return False

 main-11068675611994421723
def constraint_exists(table_name: str, constraint_name: str) -> bool:
    if not table_exists(table_name):
        return False
    bind = op.get_bind()
 main-11068675611994421723
        return True

    try:
        for c in insp.get_check_constraints(table_name):
 main-11068675611994421723
        pass

    return False
