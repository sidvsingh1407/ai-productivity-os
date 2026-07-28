import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from models.dependency_map import DependencyNode

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
