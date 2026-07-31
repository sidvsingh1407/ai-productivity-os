import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Optional, Literal

NodeType = Literal['ai_system', 'workflow', 'audit']
# Placeholder enum for edge types, to be expanded in future tickets.
EdgeType = Literal['uses', 'depends_on', 'feeds_into', 'integration', 'escalates_to']

class DependencyNodeBase(BaseModel):
    node_type: NodeType
    ai_system_id: Optional[uuid.UUID] = None
    workflow_id: Optional[uuid.UUID] = None
    audit_id: Optional[uuid.UUID] = None

    @model_validator(mode='after')
    def check_node_type_alignment(self) -> 'DependencyNodeBase':
        node_type = self.node_type
        if node_type == 'ai_system' and (self.ai_system_id is None or self.workflow_id is not None or self.audit_id is not None):
            raise ValueError("For node_type 'ai_system', only ai_system_id must be provided.")
        elif node_type == 'workflow' and (self.workflow_id is None or self.ai_system_id is not None or self.audit_id is not None):
            raise ValueError("For node_type 'workflow', only workflow_id must be provided.")
        elif node_type == 'audit' and (self.audit_id is None or self.ai_system_id is not None or self.workflow_id is not None):
            raise ValueError("For node_type 'audit', only audit_id must be provided.")
        return self

class DependencyNodeCreate(DependencyNodeBase):
    pass

class DependencyNodeResponse(DependencyNodeBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ImpactScore(BaseModel):
    total_score: int = Field(default=0, description="Total impact score 0-100")
    criticality_score: int = Field(default=0, description="Score derived from AI System criticality")
    findings_score: int = Field(default=0, description="Score derived from max finding severity")
    risk_level_score: int = Field(default=0, description="Score derived from latest risk classification")
    is_unscored_node: bool = Field(default=False, description="Flag indicating if the node could not be scored (e.g. workflow without connected AI systems)")


class TraversedNode(DependencyNodeResponse):
    impact: ImpactScore
    depth: int = Field(..., description="Depth of this node from the traversal origin")


class ImpactAnalysisResponse(BaseModel):
    origin_node: DependencyNodeResponse
    origin_impact: ImpactScore
    depends_on: list[TraversedNode] = Field(default_factory=list, description="Nodes that the origin node depends on (outward traversal)")
    used_by: list[TraversedNode] = Field(default_factory=list, description="Nodes that depend on the origin node (inward traversal)")


class DependencyEdgeBase(BaseModel):
    source_node_id: uuid.UUID
    target_node_id: uuid.UUID
    edge_type: EdgeType = Field(..., description="The type of relationship between the nodes")

class DependencyEdgeCreate(DependencyEdgeBase):
    pass

class DependencyEdgeResponse(DependencyEdgeBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
