from typing import Dict, Any, List

def generate_workflow_intelligence(input_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates deterministic operational intelligence from workflow input data.
    """
    description = input_config.get("workflowDescription", "").lower()
    challenges = input_config.get("currentChallenges", "").lower()
    tools = input_config.get("currentToolsUsed", "").lower()
    team_size = input_config.get("teamSize", "")
    department = input_config.get("department", "")

    # Combine text for easier matching
    full_text = f"{description} {challenges} {tools}"

    bottlenecks = _generate_bottlenecks(full_text, description, challenges, tools)

    # Calculate maturity based on bottlenecks and indicators
    maturity = _determine_maturity(full_text, bottlenecks)

    # Generate Risks
    risks = _generate_risks(full_text, bottlenecks)

    # Generate Recommendations
    recommendations = _generate_recommendations(bottlenecks, full_text)

    # Derive top items
    most_critical_bottleneck = "No critical bottlenecks identified."
    primary_root_cause = "Operations appear stable."
    highest_priority_intervention = "Continue current operational optimization."
    workflow_risk_level = "Low"

    if bottlenecks:
        # Sort bottlenecks by severity: Critical > Major > Moderate > Advisory
        severity_rank = {"Critical": 4, "Major": 3, "Moderate": 2, "Advisory": 1}
        sorted_bottlenecks = sorted(bottlenecks, key=lambda x: severity_rank.get(x["severity"], 0), reverse=True)
        top_bottleneck = sorted_bottlenecks[0]
        most_critical_bottleneck = top_bottleneck["title"]
        primary_root_cause = top_bottleneck["root_cause"]["root_cause"]

    if recommendations:
        priority_rank = {"Immediate": 3, "Near-Term": 2, "Long-Term": 1}
        sorted_recs = sorted(recommendations, key=lambda x: priority_rank.get(x["priority"], 0), reverse=True)
        highest_priority_intervention = sorted_recs[0]["recommendation"]

    if risks:
        risk_rank = {"High": 3, "Medium": 2, "Low": 1}
        highest_risk = max(risks, key=lambda x: risk_rank.get(x["workflow_risk"], 0))
        workflow_risk_level = highest_risk["workflow_risk"]

    executive_summary = {
        "most_critical_bottleneck": most_critical_bottleneck,
        "primary_root_cause": primary_root_cause,
        "highest_priority_intervention": highest_priority_intervention,
        "workflow_risk_level": workflow_risk_level,
        "workflow_maturity": maturity
    }

    return {
        "executive_summary": executive_summary,
        "workflow_maturity": maturity,
        "workflow_risk_level": workflow_risk_level,
        "most_critical_bottleneck": most_critical_bottleneck,
        "primary_root_cause": primary_root_cause,
        "highest_priority_intervention": highest_priority_intervention,
        "bottlenecks": bottlenecks,
        "risks": risks,
        "recommendations": recommendations
    }

def _generate_bottlenecks(full_text: str, description: str, challenges: str, tools: str) -> List[Dict[str, Any]]:
    bottlenecks = []

    # 1. Manual Approval Dependencies
    if any(word in full_text for word in ["approval", "approve", "sign-off", "manager review", "decision", "bottleneck"]):
        if any(word in challenges for word in ["delay", "wait", "slow", "bottleneck", "stuck"]):
            bottlenecks.append({
                "title": "Manual Approval Dependencies",
                "severity": "Critical",
                "impacted_area": "Decision Making",
                "rationale": "Workflow execution is paused waiting on human authorization, leading to execution delays.",
                "root_cause": {
                    "root_cause": "Decision authority concentrated in a small number of stakeholders.",
                    "evidence": "Multiple workflow stages require sequential approvals or manual sign-off.",
                    "impact": "Slower workflow throughput and delayed execution."
                }
            })

    # 2. Data Handover Delays
    if any(word in full_text for word in ["handoff", "handover", "transfer", "email", "pass to", "send to"]):
        if any(word in challenges for word in ["lost", "missing", "incomplete", "format", "delay"]):
            bottlenecks.append({
                "title": "Data Handover Delays",
                "severity": "Major",
                "impacted_area": "Cross-Functional Collaboration",
                "rationale": "Information transfer between teams relies on unstructured communication channels.",
                "root_cause": {
                    "root_cause": "Lack of a unified system of record across teams.",
                    "evidence": "Team members must manually pass context and data via email or chat.",
                    "impact": "Context is lost, and subsequent steps require rework or clarification."
                }
            })

    # 3. Fragmented Reporting / Tooling
    tool_list = [t.strip() for t in tools.replace(",", " ").split() if t.strip()]
    if len(tool_list) > 3 or any(word in full_text for word in ["excel", "spreadsheet", "csv", "manual entry", "copy paste", "re-key"]):
        bottlenecks.append({
            "title": "Operational Fragmentation",
            "severity": "Moderate",
            "impacted_area": "Data Processing",
            "rationale": "Work is distributed across disconnected tools requiring manual bridging.",
            "root_cause": {
                "root_cause": "Lack of API integration between core operational tools.",
                "evidence": "Mention of manual spreadsheets, data entry, or disconnected systems.",
                "impact": "High risk of human error and duplicated effort."
            }
        })

    # 4. Limited Automation Coverage
    if "automation" not in full_text or any(word in full_text for word in ["manual", "by hand", "routine"]):
        if not any(word in full_text for word in ["api", "webhook", "zapier", "script"]):
            bottlenecks.append({
                "title": "Limited Automation Coverage",
                "severity": "Advisory",
                "impacted_area": "Execution Efficiency",
                "rationale": "Routine and repetitive tasks are primarily handled manually.",
                "root_cause": {
                    "root_cause": "Processes have not been formalized for systemic automation.",
                    "evidence": "Routine workflow steps are described as manual actions.",
                    "impact": "Operational scaling is constrained by human headcount."
                }
            })

    # Fallback if no specific patterns match
    if not bottlenecks:
        bottlenecks.append({
            "title": "Unoptimized Workflow Routines",
            "severity": "Advisory",
            "impacted_area": "General Operations",
            "rationale": "The workflow exhibits generic friction points that reduce optimal throughput.",
            "root_cause": {
                "root_cause": "Process steps lack standardization or systemic tooling.",
                "evidence": "General workflow description implies informal or ad-hoc task execution.",
                "impact": "Inconsistent execution times and variable output quality."
            }
        })

    return bottlenecks

def _determine_maturity(full_text: str, bottlenecks: List[Dict[str, Any]]) -> str:
    # Levels: Reactive, Developing, Managed, Optimized, Intelligent

    severity_counts = {"Critical": 0, "Major": 0, "Moderate": 0, "Advisory": 0}
    for b in bottlenecks:
        severity_counts[b["severity"]] += 1

    if severity_counts["Critical"] >= 1 or any(word in full_text for word in ["ad-hoc", "messy", "chaos", "firefighting"]):
        return "Reactive"

    if severity_counts["Major"] >= 1 or any(word in full_text for word in ["spreadsheet", "manual data", "copy paste"]):
        return "Developing"

    if any(word in full_text for word in ["standard", "process", "jira", "ticket"]):
        if severity_counts["Moderate"] > 0:
             return "Managed"

    if any(word in full_text for word in ["api", "integration", "automated", "workflow tool"]):
        return "Optimized"

    return "Intelligent"

def _generate_risks(full_text: str, bottlenecks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    risks = []

    has_critical = any(b["severity"] == "Critical" for b in bottlenecks)
    has_major = any(b["severity"] == "Major" for b in bottlenecks)

    workflow_risk = "Low"
    if has_critical:
        workflow_risk = "High"
    elif has_major:
        workflow_risk = "Medium"

    # Default risk profiles based on bottlenecks
    if any(b["title"] == "Manual Approval Dependencies" for b in bottlenecks):
        risks.append({
            "workflow_risk": workflow_risk,
            "primary_risk": "Execution Stagnation",
            "rationale": "Heavy reliance on sequential manual approvals creates high probability of workflow stalling during volume spikes or personnel absence.",
            "execution_risk": "High",
            "delay_risk": "High",
            "dependency_risk": "High",
            "scalability_risk": "High"
        })
    elif any(b["title"] == "Operational Fragmentation" for b in bottlenecks):
        risks.append({
            "workflow_risk": workflow_risk,
            "primary_risk": "Data Integrity Failure",
            "rationale": "Manual data bridging across fragmented tools significantly increases the probability of transcription errors and data loss.",
            "execution_risk": "Medium",
            "delay_risk": "Medium",
            "dependency_risk": "Low",
            "scalability_risk": "High"
        })
    else:
        risks.append({
            "workflow_risk": workflow_risk,
            "primary_risk": "Operational Inefficiency",
            "rationale": "Current workflow patterns restrict maximum throughput and require disproportionate human effort to maintain.",
            "execution_risk": "Low",
            "delay_risk": "Medium",
            "dependency_risk": "Low",
            "scalability_risk": "Medium"
        })

    return risks

def _generate_recommendations(bottlenecks: List[Dict[str, Any]], full_text: str) -> List[Dict[str, Any]]:
    recommendations = []

    for b in bottlenecks:
        if b["title"] == "Manual Approval Dependencies":
            recommendations.append({
                "recommendation": "Introduce parallel approval paths or threshold-based auto-approvals.",
                "priority": "Immediate",
                "expected_impact": "Reduce approval cycle time and eliminate single-point-of-failure delays.",
                "implementation_effort": "Medium"
            })
        elif b["title"] == "Data Handover Delays":
            recommendations.append({
                "recommendation": "Standardize handoff payloads using a shared system of record or ticketing system.",
                "priority": "Immediate",
                "expected_impact": "Prevent context loss and reduce rework caused by incomplete information.",
                "implementation_effort": "Medium"
            })
        elif b["title"] == "Operational Fragmentation":
            recommendations.append({
                "recommendation": "Implement API-based synchronization between core operational tools.",
                "priority": "Near-Term",
                "expected_impact": "Eliminate manual data entry errors and ensure data consistency across platforms.",
                "implementation_effort": "High"
            })
        elif b["title"] == "Limited Automation Coverage":
            recommendations.append({
                "recommendation": "Identify repetitive, rule-based steps for RPA or script-based automation.",
                "priority": "Near-Term",
                "expected_impact": "Free up human capacity for higher-value cognitive tasks.",
                "implementation_effort": "Low"
            })

    if not recommendations:
         recommendations.append({
             "recommendation": "Conduct a time-motion study to identify hidden friction points.",
             "priority": "Long-Term",
             "expected_impact": "Uncover qualitative workflow issues not immediately apparent in self-reporting.",
             "implementation_effort": "Medium"
         })

    return recommendations
