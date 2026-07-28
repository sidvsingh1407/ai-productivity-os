"""add dependency map tables

Revision ID: 57c60c110565
Revises: fe73948a5cfc
Create Date: 2026-07-28 03:06:40.610260

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '57c60c110565'
down_revision: Union[str, Sequence[str], None] = 'fe73948a5cfc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'dependency_nodes',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('organization_id', sa.Uuid(), nullable=False),
        sa.Column('node_type', sa.String(), nullable=False),
        sa.Column('ai_system_id', sa.Uuid(), nullable=True),
        sa.Column('workflow_id', sa.Uuid(), nullable=True),
        sa.Column('audit_id', sa.Uuid(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.CheckConstraint(
            "(ai_system_id IS NOT NULL AND workflow_id IS NULL AND audit_id IS NULL AND node_type = 'ai_system') OR "
            "(workflow_id IS NOT NULL AND ai_system_id IS NULL AND audit_id IS NULL AND node_type = 'workflow') OR "
            "(audit_id IS NOT NULL AND ai_system_id IS NULL AND workflow_id IS NULL AND node_type = 'audit')",
            name='check_node_type_fk_alignment'
        ),
        sa.ForeignKeyConstraint(['ai_system_id'], ['ai_systems.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['audit_id'], ['audits.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['workflow_id'], ['workflows.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dependency_nodes_ai_system_id'), 'dependency_nodes', ['ai_system_id'], unique=False)
    op.create_index(op.f('ix_dependency_nodes_audit_id'), 'dependency_nodes', ['audit_id'], unique=False)
    op.create_index(op.f('ix_dependency_nodes_organization_id'), 'dependency_nodes', ['organization_id'], unique=False)
    op.create_index(op.f('ix_dependency_nodes_workflow_id'), 'dependency_nodes', ['workflow_id'], unique=False)

    op.create_table(
        'dependency_edges',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('organization_id', sa.Uuid(), nullable=False),
        sa.Column('source_node_id', sa.Uuid(), nullable=False),
        sa.Column('target_node_id', sa.Uuid(), nullable=False),
        sa.Column('edge_type', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['source_node_id'], ['dependency_nodes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['target_node_id'], ['dependency_nodes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dependency_edges_organization_id'), 'dependency_edges', ['organization_id'], unique=False)
    op.create_index(op.f('ix_dependency_edges_source_node_id'), 'dependency_edges', ['source_node_id'], unique=False)
    op.create_index(op.f('ix_dependency_edges_target_node_id'), 'dependency_edges', ['target_node_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_dependency_edges_target_node_id'), table_name='dependency_edges')
    op.drop_index(op.f('ix_dependency_edges_source_node_id'), table_name='dependency_edges')
    op.drop_index(op.f('ix_dependency_edges_organization_id'), table_name='dependency_edges')
    op.drop_table('dependency_edges')

    op.drop_index(op.f('ix_dependency_nodes_workflow_id'), table_name='dependency_nodes')
    op.drop_index(op.f('ix_dependency_nodes_organization_id'), table_name='dependency_nodes')
    op.drop_index(op.f('ix_dependency_nodes_audit_id'), table_name='dependency_nodes')
    op.drop_index(op.f('ix_dependency_nodes_ai_system_id'), table_name='dependency_nodes')
    op.drop_table('dependency_nodes')
