import uuid
from typing import Dict, List, Set, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, desc

from models.dependency_map import DependencyNode, DependencyEdge
from models.ai_system import AISystem
from models.risk_classification import RiskClassification
from models.system_finding import SystemFinding
from dependency_map.schemas import ImpactScore, TraversedNode, ImpactAnalysisResponse

# Scoring Constants
CRITICALITY_SCORES = {
    "critical": 30,
    "high": 20,
    "medium": 10
}

FINDING_SEVERITY_SCORES = {
    "Critical": 40,
    "Major": 30,
    "Moderate": 20,
    "Advisory": 10
}

RISK_LEVEL_SCORES = {
    "unacceptable": 30,
    "high_risk": 25,
    "ambiguous": 15,
    "limited_risk": 10,
    "minimal_risk": 0
}

async def calculate_ai_system_impacts(
    db: AsyncSession,
    ai_system_nodes: List[DependencyNode]
) -> Dict[uuid.UUID, ImpactScore]:
    """Calculate the deterministic impact score for given AI system nodes."""
    if not ai_system_nodes:
        return {}

    system_ids = [node.ai_system_id for node in ai_system_nodes if node.ai_system_id]
    if not system_ids:
        return {}

    # 1. Fetch AISystems to get criticality
    systems_stmt = select(AISystem).where(AISystem.id.in_(system_ids))
    systems_result = await db.execute(systems_stmt)
    systems = {sys.id: sys for sys in systems_result.scalars().all()}

    # 2. Fetch RiskClassifications (latest per system)
    risk_stmt = select(RiskClassification).where(
        RiskClassification.ai_system_id.in_(system_ids)
    ).order_by(
        RiskClassification.ai_system_id,
        desc(RiskClassification.created_at)
    )
    risk_result = await db.execute(risk_stmt)
    # We want the most recent row per system_id. Since we order by created_at desc,
    # the first row we see for a given system_id is the most recent one.
    latest_risks = {}
    for risk in risk_result.scalars().all():
        if risk.ai_system_id not in latest_risks:
            latest_risks[risk.ai_system_id] = risk

    # 3. Fetch SystemFindings (to get max finding severity)
    findings_stmt = select(SystemFinding).where(
        SystemFinding.ai_system_id.in_(system_ids)
    )
    findings_result = await db.execute(findings_stmt)

    system_findings_map = {}
    for sf in findings_result.scalars().all():
        if sf.ai_system_id not in system_findings_map:
            system_findings_map[sf.ai_system_id] = []
        system_findings_map[sf.ai_system_id].extend(sf.findings)

    # 4. Calculate Scores
    impact_scores: Dict[uuid.UUID, ImpactScore] = {}
    for node in ai_system_nodes:
        sys_id = node.ai_system_id
        sys = systems.get(sys_id)

        # Base Criticality
        criticality = (sys.criticality or "").lower() if sys else ""
        criticality_score = CRITICALITY_SCORES.get(criticality, 0)

        # Risk Level
        risk = latest_risks.get(sys_id)
        risk_level = risk.risk_level if risk else ""
        risk_level_score = RISK_LEVEL_SCORES.get(risk_level, 0)

        # Max Finding Severity
        findings = system_findings_map.get(sys_id, [])
        max_finding_score = 0
        for f in findings:
            severity = f.get("severity", "")
            score = FINDING_SEVERITY_SCORES.get(severity, 0)
            if score > max_finding_score:
                max_finding_score = score

        total = criticality_score + risk_level_score + max_finding_score
        impact_scores[node.id] = ImpactScore(
            total_score=total,
            criticality_score=criticality_score,
            findings_score=max_finding_score,
            risk_level_score=risk_level_score,
            is_unscored_node=False
        )

    return impact_scores

async def traverse_and_analyze(
    db: AsyncSession,
    organization_id: uuid.UUID,
    origin_node: DependencyNode,
    max_depth: int = 2
) -> ImpactAnalysisResponse:

    # Trackers
    # Keep dicts of node_id -> (node, depth) for each direction
    outward_nodes: Dict[uuid.UUID, tuple[DependencyNode, int]] = {} # depends_on
    inward_nodes: Dict[uuid.UUID, tuple[DependencyNode, int]] = {} # used_by

    # 1. Outward Traversal (depends_on: edges where source == current)
    current_outward_ids = {origin_node.id}
    for depth in range(1, max_depth + 1):
        if not current_outward_ids:
            break

        stmt = select(DependencyEdge, DependencyNode).join(
            DependencyNode, DependencyNode.id == DependencyEdge.target_node_id
        ).where(
            DependencyEdge.organization_id == organization_id,
            DependencyEdge.source_node_id.in_(current_outward_ids)
        )
        result = await db.execute(stmt)
        next_ids = set()
        for edge, node in result.all():
            if node.id not in outward_nodes and node.id != origin_node.id:
                outward_nodes[node.id] = (node, depth)
                next_ids.add(node.id)
        current_outward_ids = next_ids

    # 2. Inward Traversal (used_by: edges where target == current)
    current_inward_ids = {origin_node.id}
    for depth in range(1, max_depth + 1):
        if not current_inward_ids:
            break

        stmt = select(DependencyEdge, DependencyNode).join(
            DependencyNode, DependencyNode.id == DependencyEdge.source_node_id
        ).where(
            DependencyEdge.organization_id == organization_id,
            DependencyEdge.target_node_id.in_(current_inward_ids)
        )
        result = await db.execute(stmt)
        next_ids = set()
        for edge, node in result.all():
            if node.id not in inward_nodes and node.id != origin_node.id:
                inward_nodes[node.id] = (node, depth)
                next_ids.add(node.id)
        current_inward_ids = next_ids

    all_traversed_nodes = []
    for node, _ in outward_nodes.values():
        all_traversed_nodes.append(node)
    for node, _ in inward_nodes.values():
        all_traversed_nodes.append(node)

    # Add origin to scoring batch
    all_nodes_to_score = all_traversed_nodes + [origin_node]

    # Separate into ai_systems and others
    ai_system_nodes = [n for n in all_nodes_to_score if n.node_type == 'ai_system']
    other_nodes = [n for n in all_nodes_to_score if n.node_type != 'ai_system']

    # 3. Calculate impacts for AI Systems
    impact_scores = await calculate_ai_system_impacts(db, ai_system_nodes)

    # 4. Infer impacts for Workflows/Audits
    for node in other_nodes:
        # For non-AI nodes, we need to find AI systems connected to it *in the traversed subgraph*.
        # We look at all edges connected to this node in our subgraph (including origin if connected).

        # Determine the set of nodes in the subgraph
        subgraph_node_ids = {n.id for n in all_nodes_to_score}

        # Find edges connected to this node (in any direction) within the subgraph
        connected_stmt = select(DependencyEdge).where(
            DependencyEdge.organization_id == organization_id,
            or_(
                DependencyEdge.source_node_id == node.id,
                DependencyEdge.target_node_id == node.id
            )
        )
        connected_result = await db.execute(connected_stmt)
        connected_edges = connected_result.scalars().all()

        connected_ai_system_ids = set()
        for e in connected_edges:
            neighbor_id = e.target_node_id if e.source_node_id == node.id else e.source_node_id
            if neighbor_id in subgraph_node_ids and neighbor_id in impact_scores: # it's an ai_system in subgraph
                connected_ai_system_ids.add(neighbor_id)

        if not connected_ai_system_ids:
            impact_scores[node.id] = ImpactScore(is_unscored_node=True)
        else:
            # Get max score components from connected AI systems
            max_total = 0
            max_crit = 0
            max_find = 0
            max_risk = 0
            for neighbor_id in connected_ai_system_ids:
                sc = impact_scores[neighbor_id]
                max_total = max(max_total, sc.total_score)
                max_crit = max(max_crit, sc.criticality_score)
                max_find = max(max_find, sc.findings_score)
                max_risk = max(max_risk, sc.risk_level_score)

            impact_scores[node.id] = ImpactScore(
                total_score=max_total,
                criticality_score=max_crit,
                findings_score=max_find,
                risk_level_score=max_risk,
                is_unscored_node=False
            )

    # Assemble response
    def to_traversed(node: DependencyNode, depth: int) -> TraversedNode:
        return TraversedNode(
            id=node.id,
            organization_id=node.organization_id,
            created_at=node.created_at,
            updated_at=node.updated_at,
            node_type=node.node_type,
            ai_system_id=node.ai_system_id,
            workflow_id=node.workflow_id,
            audit_id=node.audit_id,
            impact=impact_scores[node.id],
            depth=depth
        )

    depends_on = [to_traversed(n, d) for n, d in outward_nodes.values()]
    used_by = [to_traversed(n, d) for n, d in inward_nodes.values()]

    return ImpactAnalysisResponse(
        origin_node=origin_node,
        origin_impact=impact_scores[origin_node.id],
        depends_on=depends_on,
        used_by=used_by
    )
