"""add missing tables opportunities risk_classifications agent_recommendations

Revision ID: a4da25a47216
Revises: 45d20f343cfe
Create Date: 2024-06-25 12:05:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from migration_helpers import table_exists

# revision identifiers, used by Alembic.
revision: str = 'a4da25a47216'
down_revision: Union[str, Sequence[str], None] = '45d20f343cfe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. risk_classifications
    if not table_exists('risk_classifications'):
        op.create_table(
            'risk_classifications',
            sa.Column('id', sa.UUID(), nullable=False),
            sa.Column('audit_id', sa.UUID(), nullable=False),
            sa.Column('ai_system_id', sa.UUID(), nullable=False),
            sa.Column('risk_level', sa.String(), nullable=False),
            sa.Column('matched_category', sa.String(), nullable=True),
            sa.Column('rationale', sa.Text(), nullable=False),
            sa.Column('citation_reference', sa.Text(), nullable=False),
            sa.Column('requires_human_review', sa.Boolean(), server_default='false', nullable=False),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.ForeignKeyConstraint(['ai_system_id'], ['ai_systems.id'], ),
            sa.ForeignKeyConstraint(['audit_id'], ['audits.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_risk_classifications_ai_system_id'), 'risk_classifications', ['ai_system_id'], unique=False)
        op.create_index(op.f('ix_risk_classifications_audit_id'), 'risk_classifications', ['audit_id'], unique=False)

        op.execute("ALTER TABLE public.risk_classifications ENABLE ROW LEVEL SECURITY;")
        op.execute("""
            DO $$
            BEGIN
                IF EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'anon') THEN
                    EXECUTE 'REVOKE ALL ON public.risk_classifications FROM anon;';
                END IF;
                IF EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'authenticated') THEN
                    EXECUTE 'REVOKE ALL ON public.risk_classifications FROM authenticated;';
                END IF;
            END
            $$;
        """)

    # 2. opportunities
    if not table_exists('opportunities'):
        op.create_table(
            'opportunities',
            sa.Column('id', sa.UUID(), nullable=False),
            sa.Column('organization_id', sa.UUID(), nullable=False),
            sa.Column('ai_system_id', sa.UUID(), nullable=True),
            sa.Column('category', sa.String(), nullable=False),
            sa.Column('title', sa.String(), nullable=False),
            sa.Column('description', sa.String(), nullable=False),
            sa.Column('source_module', sa.String(), nullable=False),
            sa.Column('confidence_or_priority', sa.String(), nullable=False),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.ForeignKeyConstraint(['ai_system_id'], ['ai_systems.id'], ondelete='CASCADE'),
            sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_opportunities_ai_system_id'), 'opportunities', ['ai_system_id'], unique=False)
        op.create_index(op.f('ix_opportunities_organization_id'), 'opportunities', ['organization_id'], unique=False)

        op.execute("ALTER TABLE public.opportunities ENABLE ROW LEVEL SECURITY;")
        op.execute("""
            DO $$
            BEGIN
                IF EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'anon') THEN
                    EXECUTE 'REVOKE ALL ON public.opportunities FROM anon;';
                END IF;
                IF EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'authenticated') THEN
                    EXECUTE 'REVOKE ALL ON public.opportunities FROM authenticated;';
                END IF;
            END
            $$;
        """)

    # 3. agent_recommendations
    if not table_exists('agent_recommendations'):
        op.create_table(
            'agent_recommendations',
            sa.Column('id', sa.UUID(), nullable=False),
            sa.Column('organization_id', sa.UUID(), nullable=False),
            sa.Column('opportunity_id', sa.UUID(), nullable=False),
            sa.Column('agent_type', sa.String(), nullable=False),
            sa.Column('rationale', sa.String(), nullable=False),
            sa.Column('confidence', sa.String(), nullable=False),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.ForeignKeyConstraint(['opportunity_id'], ['opportunities.id'], ondelete='CASCADE'),
            sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('opportunity_id', 'agent_type', name='uix_opportunity_agent_type')
        )
        op.create_index(op.f('ix_agent_recommendations_opportunity_id'), 'agent_recommendations', ['opportunity_id'], unique=False)
        op.create_index(op.f('ix_agent_recommendations_organization_id'), 'agent_recommendations', ['organization_id'], unique=False)

        op.execute("ALTER TABLE public.agent_recommendations ENABLE ROW LEVEL SECURITY;")
        op.execute("""
            DO $$
            BEGIN
                IF EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'anon') THEN
                    EXECUTE 'REVOKE ALL ON public.agent_recommendations FROM anon;';
                END IF;
                IF EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'authenticated') THEN
                    EXECUTE 'REVOKE ALL ON public.agent_recommendations FROM authenticated;';
                END IF;
            END
            $$;
        """)


def downgrade() -> None:
    if table_exists('agent_recommendations'):
        op.drop_table('agent_recommendations')

    if table_exists('opportunities'):
        op.drop_table('opportunities')

    if table_exists('risk_classifications'):
        op.drop_table('risk_classifications')
