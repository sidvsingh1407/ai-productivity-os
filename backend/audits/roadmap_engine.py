from typing import Dict, List, Any

def generate_roadmap(
    total_score: int,
    dimension_scores: Dict[str, int],
    findings: List[Dict[str, Any]],
    recommendations: List[Dict[str, Any]],
    severity_levels: Dict[str, str]
) -> Dict[str, Dict[str, List[Dict[str, str]]]]:
    """
    Generates a deterministic 30, 60, and 90-day implementation roadmap based on assessment results.
    """

    # Roadmap actions buckets
    roadmap = {
        "day_30": [],
        "day_60": [],
        "day_90": []
    }

    # Internal mappings for action generation
    # Structure:
    # DIMENSION_RULES[dimension][maturity_band][time_horizon] = (Action, Reason)
    # Maturity bands: "low" (< 40), "moderate" (40-69), "high" (>= 70)
    DIMENSION_RULES = {
        "governance": {
            "low": {
                "day_30": ("Establish AI Governance Committee and designate ownership", "Governance maturity is critically low, requiring immediate leadership alignment.", "Critical"),
                "day_60": ("Draft and publish foundational AI usage policies", "Clear guidelines are needed to prevent unauthorized or risky AI adoption.", "High"),
                "day_90": ("Implement mandatory compliance and risk review process", "Long-term risk mitigation requires formal approval workflows.", "High")
            },
            "moderate": {
                "day_30": ("Review and refine existing AI governance framework", "Current governance exists but needs structural improvement.", "Medium"),
                "day_60": ("Formalize AI tool request and approval workflows", "Standardizing the intake process reduces friction and shadow IT.", "Medium"),
                "day_90": ("Conduct audit of current AI deployments against policy", "Ensuring alignment between policy and actual usage.", "Medium")
            },
            "high": {
                "day_30": ("Evaluate governance structure for scalability", "Mature governance should be assessed for friction and speed.", "Low"),
                "day_60": ("Automate compliance and security monitoring", "Scaling governance requires automated oversight mechanisms.", "Low"),
                "day_90": ("Benchmark governance practices against industry leaders", "Continuous improvement through external validation.", "Low")
            }
        },
        "adoption": {
            "low": {
                "day_30": ("Identify current AI usage and shadow IT instances", "Visibility into informal adoption is required to establish control.", "Critical"),
                "day_60": ("Select 1-2 high-value, low-risk pilot use cases", "Demonstrating controlled value builds momentum and trust.", "High"),
                "day_90": ("Develop standardized playbooks for approved tools", "Users need formal guidance to maximize tool effectiveness.", "High")
            },
            "moderate": {
                "day_30": ("Map successful AI usage patterns across departments", "Identifying internal best practices for broader distribution.", "Medium"),
                "day_60": ("Expand AI pilots to adjacent teams and workflows", "Scaling adoption beyond initial successful pockets.", "Medium"),
                "day_90": ("Establish an internal AI center of excellence or community", "Peer-led knowledge sharing accelerates organic adoption.", "Medium")
            },
            "high": {
                "day_30": ("Audit advanced AI use cases for enterprise expansion", "Identifying opportunities for organization-wide transformation.", "Low"),
                "day_60": ("Integrate AI enablement into standard onboarding", "Institutionalizing AI competency for all new hires.", "Low"),
                "day_90": ("Develop custom AI capabilities for specialized workflows", "Moving beyond off-the-shelf tools to proprietary advantage.", "Low")
            }
        },
        "integration": {
            "low": {
                "day_30": ("Map core operational workflows and data dependencies", "Understanding the current state is necessary before integration.", "High"),
                "day_60": ("Identify systems causing major workflow bottlenecks", "Pinpointing friction areas where integration yields the highest ROI.", "High"),
                "day_90": ("Implement targeted API integrations for critical workflows", "Connecting disjointed systems to reduce manual intervention.", "High")
            },
            "moderate": {
                "day_30": ("Audit existing system integrations for efficiency", "Assessing current automation to identify optimization areas.", "Medium"),
                "day_60": ("Automate repetitive cross-platform data transfers", "Reducing manual data entry and improving data consistency.", "Medium"),
                "day_90": ("Establish continuous monitoring for integrated workflows", "Ensuring reliability and performance of automated processes.", "Medium")
            },
            "high": {
                "day_30": ("Evaluate architecture for advanced AI integration readiness", "Preparing systems for deep, predictive, or generative AI layers.", "Low"),
                "day_60": ("Implement intelligent workflow routing and orchestration", "Moving from basic automation to dynamic process management.", "Low"),
                "day_90": ("Scale integrated AI solutions across the enterprise ecosystem", "Maximizing the leverage of a mature, connected architecture.", "Low")
            }
        },
        "awareness": {
            "low": {
                "day_30": ("Conduct baseline AI literacy assessment across organization", "Understanding the knowledge gap is the first step to closing it.", "High"),
                "day_60": ("Launch foundational AI awareness communication campaign", "Aligning the organization on AI capabilities and strategic intent.", "Medium"),
                "day_90": ("Deliver role-specific AI training for key departments", "Targeted education translates general awareness into practical skill.", "Medium")
            },
            "moderate": {
                "day_30": ("Assess effectiveness of current AI training programs", "Evaluating what educational initiatives are working.", "Medium"),
                "day_60": ("Develop advanced training modules for power users", "Cultivating internal experts to drive departmental innovation.", "Medium"),
                "day_90": ("Implement continuous learning program for AI advancements", "Keeping the workforce updated on rapidly evolving technology.", "Medium")
            },
            "high": {
                "day_30": ("Review external knowledge sharing and industry presence", "Leveraging internal expertise for external thought leadership.", "Low"),
                "day_60": ("Host internal AI innovation showcases or hackathons", "Fostering a culture of continuous AI-driven innovation.", "Low"),
                "day_90": ("Establish partnerships with academic or industry AI bodies", "Maintaining a leading edge in AI developments and talent.", "Low")
            }
        },
        "roi": {
            "low": {
                "day_30": ("Define clear business objectives and success criteria for AI", "Without defined goals, value measurement is impossible.", "Critical"),
                "day_60": ("Establish baseline metrics for workflows pre-AI adoption", "A baseline is required to measure subsequent improvements.", "High"),
                "day_90": ("Implement a standardized ROI tracking framework", "Formalizing how AI investments are evaluated against outcomes.", "High")
            },
            "moderate": {
                "day_30": ("Review current ROI tracking for accuracy and completeness", "Ensuring value measurement captures both hard and soft costs.", "Medium"),
                "day_60": ("Refine metrics to capture operational quality and speed", "Moving beyond simple cost savings to value generation metrics.", "Medium"),
                "day_90": ("Create executive dashboards for AI portfolio performance", "Providing leadership with visibility into AI investment returns.", "Medium")
            },
            "high": {
                "day_30": ("Conduct advanced attribution modeling for AI impact", "Precisely isolating the financial impact of AI initiatives.", "Low"),
                "day_60": ("Optimize AI portfolio allocation based on historical ROI", "Directing resources to the most efficient and effective initiatives.", "Low"),
                "day_90": ("Publish comprehensive internal report on AI value realization", "Demonstrating transparent value delivery to stakeholders.", "Low")
            }
        }
    }

    # Extract dimensions and determine their maturity band
    # We expect dimension scores to be scaled out of 100 or out of 20.
    # The requirement says:
    # Low: < 40
    # Moderate: 40-69
    # High: >= 70
    # Assuming scores passed are scaled out of 100 for these thresholds.

    # Priority rank for sorting actions
    PRIORITY_RANK = {"Critical": 1, "High": 2, "Medium": 3, "Low": 4}

    all_actions_30 = []
    all_actions_60 = []
    all_actions_90 = []

    for dim, score in dimension_scores.items():
        dim_lower = dim.lower()
        if dim_lower not in DIMENSION_RULES:
            continue

        if score < 40:
            band = "low"
        elif score < 70:
            band = "moderate"
        else:
            band = "high"

        rules = DIMENSION_RULES[dim_lower][band]

        # 30 days
        act_30, reason_30, prio_30 = rules["day_30"]
        all_actions_30.append({"action": act_30, "reason": reason_30, "priority": prio_30})

        # 60 days
        act_60, reason_60, prio_60 = rules["day_60"]
        all_actions_60.append({"action": act_60, "reason": reason_60, "priority": prio_60})

        # 90 days
        act_90, reason_90, prio_90 = rules["day_90"]
        all_actions_90.append({"action": act_90, "reason": reason_90, "priority": prio_90})

    # Sort actions by priority (Critical > High > Medium > Low)
    all_actions_30.sort(key=lambda x: PRIORITY_RANK.get(x["priority"], 99))
    all_actions_60.sort(key=lambda x: PRIORITY_RANK.get(x["priority"], 99))
    all_actions_90.sort(key=lambda x: PRIORITY_RANK.get(x["priority"], 99))

    # To ensure varied actions, if there are findings/recommendations, we might
    # inject them or use them to adjust, but for Sprint 3D rule-based logic is sufficient.
    # The requirement is 3-5 actions per time horizon.
    # We just take the top 4 (or 5) highest priority actions to meet the "3-5 actions" rule.

    # We will pick the top 4 actions across dimensions.
    # The max dimensions is 5, so picking top 4 will drop the lowest priority one.

    roadmap["day_30"] = all_actions_30[:4]
    roadmap["day_60"] = all_actions_60[:4]
    roadmap["day_90"] = all_actions_90[:4]

    return {"roadmap": roadmap}
