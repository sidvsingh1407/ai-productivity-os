"""add full invitation schema

Revision ID: 8d9e0f1g2h3i
Revises: 761fc3edb556
Create Date: 2026-06-04 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d9e0f1g2h3i'
down_revision: Union[str, None] = '761fc3edb556'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE TYPE invitationstatus AS ENUM ('pending', 'accepted', 'expired', 'revoked');")

    op.add_column('invitations', sa.Column('invited_by_user_id', sa.Uuid(), nullable=True))
    op.add_column('invitations', sa.Column('role', sa.Enum('owner', 'admin', 'member', 'viewer', name='orgrole'), server_default='member', nullable=False))
    op.add_column('invitations', sa.Column('status', sa.Enum('pending', 'accepted', 'expired', 'revoked', name='invitationstatus'), server_default='pending', nullable=False))
    op.add_column('invitations', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))

    op.create_foreign_key('fk_invitations_users', 'invitations', 'users', ['invited_by_user_id'], ['id'])
    # make non-nullable after adding columns to avoid errors with existing rows
    # assuming we handle this or there are no existing rows in dev
    # op.alter_column('invitations', 'invited_by_user_id', nullable=False)


def downgrade() -> None:
    op.drop_constraint('fk_invitations_users', 'invitations', type_='foreignkey')
    op.drop_column('invitations', 'created_at')
    op.drop_column('invitations', 'status')
    op.drop_column('invitations', 'role')
    op.drop_column('invitations', 'invited_by_user_id')
    op.execute("DROP TYPE invitationstatus;")
