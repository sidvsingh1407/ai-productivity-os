import re
from typing import Dict, Any
from prompt_intelligence.context_rules import CONTEXT_RULES, FALLBACK_CONTEXT

class ContextClassifier:
    """
    Deterministic context classifier based on keyword matching.
    """

    @staticmethod
    def _derive_environment(prompt_lower: str) -> str:
        consulting_keywords = ["consultant", "client", "engagement", "deliverable"]
        internal_ops_keywords = ["workflow", "operations", "process", "automation", "team"]
        governance_keywords = ["governance", "compliance", "policy", "audit", "regulation"]

        def count_matches(keywords: list[str]) -> int:
            return sum(1 for kw in keywords if re.search(r'\b' + re.escape(kw) + r'\b', prompt_lower))

        scores = {
            "Consulting": count_matches(consulting_keywords),
            "Internal Operations": count_matches(internal_ops_keywords),
            "Governance": count_matches(governance_keywords)
        }

        best_env = max(scores, key=scores.get)
        if scores[best_env] > 0:
            return best_env

        return "General Business Operations"

    @staticmethod
    def classify(prompt: str) -> Dict[str, Any]:
        prompt_lower = prompt.lower()

        environment = ContextClassifier._derive_environment(prompt_lower)

        category_scores = {category: 0 for category in CONTEXT_RULES}
        category_matches = {category: [] for category in CONTEXT_RULES}

        total_matches = 0

        for category, keywords in CONTEXT_RULES.items():
            for keyword in keywords:
                # Use regex to match whole words or phrases, avoiding partial matches inside words
                pattern = r'\b' + re.escape(keyword) + r'\b'
                matches = len(re.findall(pattern, prompt_lower))
                if matches > 0:
                    category_scores[category] += matches
                    total_matches += matches
                    category_matches[category].append(keyword)

        if total_matches == 0:
            return {
                "context": FALLBACK_CONTEXT,
                "environment": environment,
                "confidence": 1.0, # Complete confidence that it's fallback since no rules matched
                "reasoning": ["No matching keywords found for primary categories."]
            }

        # Find the category with the highest score
        best_category = max(category_scores, key=category_scores.get)
        winning_score = category_scores[best_category]

        # Calculate confidence
        confidence = winning_score / total_matches

        # Cap confidence at 0.95 for deterministic rules
        if confidence > 0.95:
            confidence = 0.95

        # Generate reasoning based on matched keywords for the winning category
        reasoning = []
        for keyword in category_matches[best_category]:
             reasoning.append(f"Contains language related to '{keyword}'")

        if not reasoning:
            reasoning.append("Fallback reasoning applied.")

        return {
            "context": best_category,
            "environment": environment,
            "confidence": round(confidence, 2),
            "reasoning": reasoning
        }
