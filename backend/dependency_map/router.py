import uuid
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from dependencies import get_current_org, require_role
from dependency_map import schemas, service
from models.organization import Organization

router = APIRouter(tags=["Dependency Map"])

# Nodes

@router.get("/nodes", response_model=List[schemas.DependencyNodeResponse], dependencies=[Depends(require_role("viewer"))])
async def list_nodes(
    org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    """List all dependency nodes for the organization."""
    return await service.get_nodes(db, organization_id=org.id)

@router.post("/nodes/get-or-create", response_model=schemas.DependencyNodeResponse, dependencies=[Depends(require_role("member"))])
async def get_or_create_node(
    node_data: schemas.DependencyNodeCreate,
    org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    """
    Get an existing dependency node for an entity, or create it if it doesn't exist.
    """
    return await service.get_or_create_node(db, organization_id=org.id, node_data=node_data)

@router.post("/nodes", response_model=schemas.DependencyNodeResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role("member"))])
async def create_node(
    node_data: schemas.DependencyNodeCreate,
    org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    """Create a new dependency node."""
    return await service.create_node(db, organization_id=org.id, node_data=node_data)

@router.get("/nodes/{node_id}", response_model=schemas.DependencyNodeResponse, dependencies=[Depends(require_role("viewer"))])
async def get_node(
    node_id: uuid.UUID,
    org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific dependency node."""
    return await service.get_node(db, organization_id=org.id, node_id=node_id)


@router.delete("/nodes/{node_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role("member"))])
async def delete_node(
    node_id: uuid.UUID,
    org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    """Delete a dependency node."""
    await service.delete_node(db, organization_id=org.id, node_id=node_id)


# Edges

@router.get("/edges", response_model=List[schemas.DependencyEdgeResponse], dependencies=[Depends(require_role("viewer"))])
async def list_edges(
    org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    """List all dependency edges for the organization."""
    return await service.get_edges(db, organization_id=org.id)

@router.post("/edges", response_model=schemas.DependencyEdgeResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role("member"))])
async def create_edge(
    edge_data: schemas.DependencyEdgeCreate,
    org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    """Create a new dependency edge."""
    return await service.create_edge(db, organization_id=org.id, edge_data=edge_data)

@router.get("/edges/{edge_id}", response_model=schemas.DependencyEdgeResponse, dependencies=[Depends(require_role("viewer"))])
async def get_edge(
    edge_id: uuid.UUID,
    org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific dependency edge."""
    return await service.get_edge(db, organization_id=org.id, edge_id=edge_id)

@router.delete("/edges/{edge_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role("member"))])
async def delete_edge(
    edge_id: uuid.UUID,
    org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    """Delete a dependency edge."""
    await service.delete_edge(db, organization_id=org.id, edge_id=edge_id)
