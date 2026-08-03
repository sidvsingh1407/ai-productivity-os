from typing import List, Dict, Any, Optional
import uuid

def generate_opportunities(
    adoption_records: List[Dict[str, Any]],
    workflows: List[Dict[str, Any]],
    ai_systems: List[Dict[str, Any]],
    engineering_records: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    opportunities = []

    # 1. Adoption (6.1)
    # Fields to check: resistance_level, training_status, shadow_ai_detected
    for record in adoption_records:
        ai_system_id = record.get("ai_system_id")
        org_id = record.get("organization_id")

        res_level = record.get("resistance_level", "not_specified")
        train_status = record.get("training_status", "not_specified")
        shadow_ai = record.get("shadow_ai_detected", False)

        # We must explicitly ensure we only evaluate fields if they are changed from defaults
        if res_level != "not_specified" and train_status != "not_specified":
            if res_level == "high" and train_status == "none":
                opportunities.append({
                    "organization_id": org_id,
                    "ai_system_id": ai_system_id,
                    "category": "customer_pain",  # Maps to a training/change management need
                    "title": "High Resistance & Missing Training",
                    "description": "System faces high user resistance and lacks formal training, indicating a clear need for change management or automated guidance.",
                    "source_module": "adoption",
                    "confidence_or_priority": "High"
                })

        # shadow_ai_detected defaults to False (same as "no"). User said:
        # "Only fire rules on fields that have been explicitly changed away from their default...
        # shadow_ai_detected=False vs never-assessed... only trigger on True."
        if shadow_ai is True:
            opportunities.append({
                "organization_id": org_id,
                "ai_system_id": ai_system_id,
                "category": "automation_candidate",
                "title": "Shadow AI Formalization Candidate",
                "description": "Shadow AI usage detected for this department, presenting an opportunity to formalize into a sanctioned automated process.",
                "source_module": "adoption",
                "confidence_or_priority": "Medium"
            })

    # 2. Workflows (6.2)
    # Per-Org opportunities (ai_system_id = None)
    # scores, findings (weaknesses)
    for wf in workflows:
        org_id = wf.get("org_id")
        scores = wf.get("scores", {}) or {}
        findings = wf.get("findings", {}) or {}
        weaknesses = findings.get("weaknesses", [])

        bottleneck_score = scores.get("bottleneck")
        risk_score = scores.get("risk")

        if bottleneck_score is not None and bottleneck_score < 50:
            if any("Heavy manual handoffs" in w for w in weaknesses):
                opportunities.append({
                    "organization_id": org_id,
                    "ai_system_id": None,
                    "category": "automation_candidate",
                    "title": "High Manual Workflow Bottlenecks",
                    "description": "Workflow exhibits severe bottleneck scores due to heavy manual handoffs, making it a prime candidate for automation.",
                    "source_module": "workflow",
                    "confidence_or_priority": "High"
                })

        if risk_score is not None and risk_score < 50:
            if any("fragile" in w and "bus factor" in w for w in weaknesses):
                opportunities.append({
                    "organization_id": org_id,
                    "ai_system_id": None,
                    "category": "knowledge_bottleneck",
                    "title": "Critical Knowledge Silo Risk",
                    "description": "Workflow relies heavily on single individuals with manual steps, representing a severe knowledge bottleneck.",
                    "source_module": "workflow",
                    "confidence_or_priority": "Medium"
                })

    # 3. Data Intelligence (6.3)
    # Fields: data_quality_notes, data_freshness, data_accessibility
    for sys in ai_systems:
        org_id = sys.get("organization_id")
        sys_id = sys.get("id")

        freshness = sys.get("data_freshness")
        quality = sys.get("data_quality_notes")
        access = sys.get("data_accessibility", [])

        # Check non-default/explicit inputs
        if freshness in ["static", "unknown"] and quality and len(quality.strip()) > 0:
            if len(access) > 0 and not any(a.lower() in ["api", "webhook", "database"] for a in access):
                # Meaning access is provided but only via manual exports, flat files, etc.
                opportunities.append({
                    "organization_id": org_id,
                    "ai_system_id": sys_id,
                    "category": "knowledge_bottleneck",
                    "title": "Stale Manual Data Supply",
                    "description": "System suffers from poor/static data freshness and lacks programmatic access methods, restricting data flow.",
                    "source_module": "data_intelligence",
                    "confidence_or_priority": "Medium"
                })

    # 4. Engineering Intelligence (6.4)
    # Fields: has_mlops_pipeline, monitoring_tooling, has_dedicated_prompt_engineer
    # Per-Org opportunities (ai_system_id = None)
    for eng in engineering_records:
        org_id = eng.get("organization_id")
        mlops = eng.get("has_mlops_pipeline", False)
        monitoring = eng.get("monitoring_tooling", [])
        team_size = eng.get("team_size", 0)
        prompt_eng = eng.get("has_dedicated_prompt_engineer", False)

        # We need an indicator that engineering was assessed, otherwise mlops=False and empty monitoring
        # is just the default unassessed state. We use team_size > 0 OR has_dedicated_prompt_engineer == True
        if team_size > 0 or prompt_eng is True:
            if mlops is False and len(monitoring) == 0:
                opportunities.append({
                    "organization_id": org_id,
                    "ai_system_id": None,
                    "category": "department_pain",
                    "title": "Missing MLOps Foundations",
                    "description": "AI engineering team is operating without an MLOps pipeline or monitoring tooling, limiting scalability.",
                    "source_module": "engineering",
                    "confidence_or_priority": "High"
                })

    return opportunities
