from typing import Dict, Any, List
from benchmarking.service import generate_benchmark_payload

def get_api_benchmark_payload(organization_total_score: float, organization_dimension_scores: Dict[str, float], assessments: List[Any]) -> Dict[str, Any]:
    """
    Adapter to convert the service-layer benchmark payload into the API schema format
    expected by frontend consumers (AuditDetail, Dashboard, PDF Export).
    """
    # Explicit task 4 rule check at the API boundary
    if len(assessments) < 10:
         return {
             "available": False,
             "benchmark_type": "platform",
             "message": "Insufficient benchmark data available."
         }

    try:
        service_payload = generate_benchmark_payload(
            organization_total_score=organization_total_score,
            organization_dimension_scores=organization_dimension_scores,
            assessments=assessments
        )
    except Exception as e:
        return {
             "available": False,
             "benchmark_type": "platform",
             "message": "Benchmarking service currently unavailable."
        }

    if not service_payload.get("benchmark_available"):
        return {
            "available": False,
            "benchmark_type": "platform",
            "message": service_payload.get("message", "Insufficient benchmark data available.")
        }

    # Map dimension comparisons from `your_score` to `score`
    dimension_comparisons = {}
    for dim, data in service_payload.get("dimension_comparisons", {}).items():
        dimension_comparisons[dim] = {
            "score": data.get("your_score"),
            "benchmark": data.get("benchmark"),
            "difference": data.get("difference")
        }

    # Extract insights strings from benchmark_insights
    insights = []
    benchmark_insights = service_payload.get("benchmark_insights", {})
    if overall := benchmark_insights.get("overall_summary"):
        insights.append(overall)

    if strongest := benchmark_insights.get("strongest_dimension"):
        if isinstance(strongest, dict) and strongest.get("insight"):
            insights.append(strongest.get("insight"))

    if weakest := benchmark_insights.get("weakest_dimension"):
        if isinstance(weakest, dict) and weakest.get("insight"):
            insights.append(weakest.get("insight"))

    for dim_insight in benchmark_insights.get("dimension_insights", []):
        if insight := dim_insight.get("insight"):
            insights.append(insight)

    if opportunity := benchmark_insights.get("improvement_opportunity"):
        insights.append(opportunity)

    return {
        "available": True,
        "benchmark_type": "platform",
        "sample_size": service_payload.get("sample_size"),
        "platform_average": service_payload.get("platform_average"),
        "percentile_rank": service_payload.get("percentile_rank"),
        "dimension_comparisons": dimension_comparisons,
        "insights": insights
    }
