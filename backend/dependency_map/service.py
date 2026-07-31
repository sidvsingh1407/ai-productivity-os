import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from models.dependency_map import DependencyNode, DependencyEdge
from dependency_map.schemas import (
    DependencyNodeCreate,
    DependencyEdgeCreate
)

async def validate_edge_organization_scope(
    db: AsyncSession,
    organization_id: uuid.UUID,
    source_node_id: uuid.UUID,
    target_node_id: uuid.UUID
) -> None:
    """
    Validates that both the source and target nodes exist and belong to the
    specified organization_id.
    This enforces tenant isolation for graph edges at the application layer.
    """
    # Fetch both nodes in a single query
    stmt = select(DependencyNode).where(
        DependencyNode.id.in_([source_node_id, target_node_id])
    )
    result = await db.execute(stmt)
    nodes = result.scalars().all()

    if len(nodes) != 2 and source_node_id != target_node_id:
        # If source == target, len(nodes) could be 1
        found_ids = {n.id for n in nodes}
        if source_node_id not in found_ids or target_node_id not in found_ids:
            raise HTTPException(status_code=404, detail="One or both dependency nodes not found")

    for node in nodes:
        if node.organization_id != organization_id:
            raise HTTPException(
                status_code=403,
                detail="Cross-organization dependency references are not permitted."
            )

async def get_nodes(db: AsyncSession, organization_id: uuid.UUID) -> list[DependencyNode]:
    stmt = select(DependencyNode).where(DependencyNode.organization_id == organization_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())

async def get_node(db: AsyncSession, organization_id: uuid.UUID, node_id: uuid.UUID) -> DependencyNode:
    stmt = select(DependencyNode).where(
        DependencyNode.id == node_id,
        DependencyNode.organization_id == organization_id
    )
    result = await db.execute(stmt)
    node = result.scalars().first()
    if not node:
        raise HTTPException(status_code=404, detail="Dependency node not found")
    return node

from dependency_map.impact_engine import traverse_and_analyze
from dependency_map.schemas import ImpactAnalysisResponse

async def analyze_impact(db: AsyncSession, organization_id: uuid.UUID, node_id: uuid.UUID, depth: int = 2) -> ImpactAnalysisResponse:
    node = await get_node(db, organization_id, node_id)
    return await traverse_and_analyze(db, organization_id, node, depth)

async def create_node(db: AsyncSession, organization_id: uuid.UUID, node_data: DependencyNodeCreate) -> DependencyNode:
    new_node = DependencyNode(
        organization_id=organization_id,
        node_type=node_data.node_type,
        ai_system_id=node_data.ai_system_id,
        workflow_id=node_data.workflow_id,
        audit_id=node_data.audit_id
    )
    db.add(new_node)
    try:
        await db.commit()
        await db.refresh(new_node)
        return new_node
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Failed to create node. Check if the referenced entity exists.")

async def get_or_create_node(db: AsyncSession, organization_id: uuid.UUID, node_data: DependencyNodeCreate) -> DependencyNode:
    stmt = select(DependencyNode).where(
        DependencyNode.organization_id == organization_id,
        DependencyNode.node_type == node_data.node_type
    )

    if node_data.node_type == 'ai_system':
        stmt = stmt.where(DependencyNode.ai_system_id == node_data.ai_system_id)
    elif node_data.node_type == 'workflow':
        stmt = stmt.where(DependencyNode.workflow_id == node_data.workflow_id)
    elif node_data.node_type == 'audit':
        stmt = stmt.where(DependencyNode.audit_id == node_data.audit_id)

    result = await db.execute(stmt)
    existing_node = result.scalars().first()
    if existing_node:
        return existing_node

    return await create_node(db, organization_id, node_data)

async def delete_node(db: AsyncSession, organization_id: uuid.UUID, node_id: uuid.UUID) -> None:
    node = await get_node(db, organization_id, node_id)
    await db.delete(node)
    await db.commit()

async def get_edges(db: AsyncSession, organization_id: uuid.UUID) -> list[DependencyEdge]:
    stmt = select(DependencyEdge).where(DependencyEdge.organization_id == organization_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())

async def get_edge(db: AsyncSession, organization_id: uuid.UUID, edge_id: uuid.UUID) -> DependencyEdge:
    stmt = select(DependencyEdge).where(
        DependencyEdge.id == edge_id,
        DependencyEdge.organization_id == organization_id
    )
    result = await db.execute(stmt)
    edge = result.scalars().first()
    if not edge:
        raise HTTPException(status_code=404, detail="Dependency edge not found")
    return edge

async def create_edge(db: AsyncSession, organization_id: uuid.UUID, edge_data: DependencyEdgeCreate) -> DependencyEdge:
    # 1. Reject self-referencing edges
    if edge_data.source_node_id == edge_data.target_node_id:
        raise HTTPException(status_code=400, detail="Self-referencing edges are not allowed.")

    # 2. Reject duplicate edges
    stmt = select(DependencyEdge).where(
        DependencyEdge.organization_id == organization_id,
        DependencyEdge.source_node_id == edge_data.source_node_id,
        DependencyEdge.target_node_id == edge_data.target_node_id,
        DependencyEdge.edge_type == edge_data.edge_type
    )
    result = await db.execute(stmt)
    if result.scalars().first():
        raise HTTPException(status_code=409, detail="Duplicate edge already exists.")

    # 3. Validate organization scope of nodes
    await validate_edge_organization_scope(
        db,
        organization_id,
        edge_data.source_node_id,
        edge_data.target_node_id
    )

    new_edge = DependencyEdge(
        organization_id=organization_id,
        source_node_id=edge_data.source_node_id,
        target_node_id=edge_data.target_node_id,
        edge_type=edge_data.edge_type
    )
    db.add(new_edge)
    try:
        await db.commit()
        await db.refresh(new_edge)
        return new_edge
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Failed to create edge.")

async def delete_edge(db: AsyncSession, organization_id: uuid.UUID, edge_id: uuid.UUID) -> None:
    edge = await get_edge(db, organization_id, edge_id)
    await db.delete(edge)
    await db.commit()
