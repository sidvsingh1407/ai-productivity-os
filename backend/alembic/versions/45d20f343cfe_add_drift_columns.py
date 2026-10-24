"""add drift columns

Revision ID: 45d20f343cfe
Revises: d58e9d881d0c
Create Date: 2024-06-25 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from migration_helpers import table_exists, column_exists, index_exists, constraint_exists

# revision identifiers, used by Alembic.
revision: str = '45d20f343cfe'
down_revision: Union[str, Sequence[str], None] = 'd58e9d881d0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. workflows
    if table_exists('workflows'):
        if not column_exists('workflows', 'findings'):
            op.add_column('workflows', sa.Column('findings', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
        if not column_exists('workflows', 'scores'):
            op.add_column('workflows', sa.Column('scores', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
        if not column_exists('workflows', 'steps_input'):
            op.add_column('workflows', sa.Column('steps_input', postgresql.JSONB(astext_type=sa.Text()), nullable=True))

    # 3. engineering_records
    if table_exists('engineering_records'):
        if not index_exists('engineering_records', 'ix_engineering_records_organization_id'):
            op.create_index(op.f('ix_engineering_records_organization_id'), 'engineering_records', ['organization_id'], unique=False)

    # 4. ai_systems
    if table_exists('ai_systems'):
        nullable_cols = [
            ('agent_framework', sa.String()),
            ('ai_type', sa.String()),
            ('api_provider', sa.String()),
            ('approvals_required', sa.Boolean()),
            ('authentication_method', sa.String()),
            ('business_capability', sa.String()),
            ('cloud_cost', sa.Numeric()),
            ('criticality', sa.String()),
            ('data_availability', sa.Text()),
            ('data_destinations', postgresql.JSONB(astext_type=sa.Text())),
            ('data_freshness', sa.String()),
            ('data_owner', sa.String()),
            ('data_quality_notes', sa.Text()),
            ('data_sensitivity', sa.String()),
            ('data_sources', postgresql.JSONB(astext_type=sa.Text())),
            ('department', sa.String()),
            ('expected_benefits', sa.Text()),
            ('framework', sa.String()),
            ('hosting', sa.String()),
            ('implementation_stage', sa.String()),
            ('inference_cost', sa.Numeric()),
            ('internal_external_users', sa.String()),
            ('licensing_cost', sa.Numeric()),
            ('lifecycle_status', sa.String()),
            ('maintenance_cost', sa.Numeric()),
            ('model_name', sa.String()),
            ('model_version', sa.String()),
            ('owner', sa.String()),
            ('uptime', sa.Float()),
            ('usage_frequency', sa.String()),
            ('users_count', sa.Integer()),
            ('vector_db', sa.String()),
            ('vendor', sa.String()),
            ('version', sa.String()),
            ('workflow_engine', sa.String()),
            ('cost_currency', sa.String(), "'USD'"),
            ('deployment_type', sa.String()),
            ('data_flow', sa.Text()),
            ('apis', postgresql.JSONB(astext_type=sa.Text())),
            ('databases', postgresql.JSONB(astext_type=sa.Text())),
            ('event_systems', sa.Text()),
            ('caching', sa.Text()),
            ('monitoring', sa.Text()),
            ('logging', sa.Text()),
            ('deployment_details', sa.Text()),
            ('risk_classification', sa.String()),
            ('oversight_status', sa.String()),
            ('documentation_status', sa.String()),
            ('rbac_enabled', sa.Boolean()),
            ('encryption_status', sa.String()),
            ('evidence_status', sa.String()),
            ('cost', sa.Numeric()),
            ('roi_notes', sa.Text()),
            ('licensing_type', sa.String()),
            ('planned_changes', sa.Text()),
            ('roadmap_notes', sa.Text())
        ]
        for item in nullable_cols:
            col_name = item[0]
            col_type = item[1]
            if not column_exists('ai_systems', col_name):
                if len(item) == 3:
                    # has server_default
                    op.add_column('ai_systems', sa.Column(col_name, col_type, nullable=True, server_default=sa.text(item[2])))
                else:
                    op.add_column('ai_systems', sa.Column(col_name, col_type, nullable=True))

        not_null_cols = [
            ('incident_count', sa.Integer(), '0'),
            ('applicable_policies', postgresql.JSONB(astext_type=sa.Text()), "'[]'"),
            ('applicable_regulations', postgresql.JSONB(astext_type=sa.Text()), "'[]'"),
            ('obligations', postgresql.JSONB(astext_type=sa.Text()), "'[]'"),
            ('data_accessibility', postgresql.JSONB(astext_type=sa.Text()), "'[]'"),
            ('knowledge_sources', postgresql.JSONB(astext_type=sa.Text()), "'[]'"),
            ('integrations', postgresql.JSONB(astext_type=sa.Text()), "'[]'")
        ]

        for col_name, col_type, default_val in not_null_cols:
            if not column_exists('ai_systems', col_name):
                op.add_column('ai_systems', sa.Column(col_name, col_type, nullable=False, server_default=sa.text(default_val)))


def downgrade() -> None:
    if table_exists('ai_systems'):
        cols_to_drop = ['agent_framework', 'ai_type', 'api_provider', 'approvals_required', 'authentication_method', 'business_capability', 'cloud_cost', 'cost_currency', 'criticality', 'data_accessibility', 'data_availability', 'data_destinations', 'data_freshness', 'data_owner', 'data_quality_notes', 'data_sensitivity', 'data_sources', 'department', 'expected_benefits', 'framework', 'hosting', 'implementation_stage', 'inference_cost', 'integrations', 'internal_external_users', 'knowledge_sources', 'licensing_cost', 'lifecycle_status', 'maintenance_cost', 'model_name', 'model_version', 'owner', 'uptime', 'usage_frequency', 'users_count', 'vector_db', 'vendor', 'version', 'workflow_engine', 'deployment_type', 'data_flow', 'apis', 'databases', 'event_systems', 'caching', 'monitoring', 'logging', 'deployment_details', 'risk_classification', 'oversight_status', 'documentation_status', 'rbac_enabled', 'encryption_status', 'evidence_status', 'cost', 'roi_notes', 'licensing_type', 'planned_changes', 'roadmap_notes', 'incident_count', 'applicable_policies', 'applicable_regulations', 'obligations']
        for col in cols_to_drop:
            if column_exists('ai_systems', col):
                op.drop_column('ai_systems', col)

    if table_exists('engineering_records'):
        if index_exists('engineering_records', 'ix_engineering_records_organization_id'):
            op.drop_index(op.f('ix_engineering_records_organization_id'), table_name='engineering_records')

    if table_exists('workflows'):
        if column_exists('workflows', 'steps_input'):
            op.drop_column('workflows', 'steps_input')
        if column_exists('workflows', 'scores'):
            op.drop_column('workflows', 'scores')
        if column_exists('workflows', 'findings'):
            op.drop_column('workflows', 'findings')
