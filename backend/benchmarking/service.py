from typing import List, Dict, Any, Union

def get_total_score(record: Any) -> float:
    if isinstance(record, dict):
        return float(record.get("total_score", 0) or 0)
    return float(getattr(record, "total_score", 0) or 0)

def get_dimension_scores(record: Any) -> Dict[str, float]:
    if isinstance(record, dict):
        scores = record.get("dimension_scores")
        if scores is None:
            scores = record.get("scores", {})
        return {k: float(v) for k, v in scores.items()} if scores else {}

    # Handle SQLAlchemy models or other objects
    scores = getattr(record, "dimension_scores", None)
    if scores is None:
        scores = getattr(record, "scores", {})
    return {k: float(v) for k, v in scores.items()} if scores else {}

def validate_sample_size(sample_size: int) -> Union[Dict[str, Any], None]:
    if sample_size < 10:
        return {
            "benchmark_available": False,
            "message": "Insufficient benchmark data available.",
            "sample_size": sample_size
        }
    return None

def calculate_platform_average(assessments: List[Any]) -> float:
    if not assessments:
        return 0.0
    total = sum(get_total_score(a) for a in assessments)
    return round(total / len(assessments), 1)

def calculate_dimension_averages(assessments: List[Any]) -> Dict[str, int]:
    if not assessments:
        return {}

    dimension_totals = {}
    dimension_counts = {}

    for assessment in assessments:
        scores = get_dimension_scores(assessment)
        for dim, score in scores.items():
            dimension_totals[dim] = dimension_totals.get(dim, 0) + score
            dimension_counts[dim] = dimension_counts.get(dim, 0) + 1

    averages = {}
    for dim, total in dimension_totals.items():
        count = dimension_counts[dim]
        if count > 0:
            averages[dim] = int(round(total / count))

    return averages

def calculate_percentile_rank(organization_score: float, assessments: List[Any]) -> int:
    if not assessments:
        return 0

    number_below = 0
    number_equal = 0
    total = len(assessments)

    for assessment in assessments:
        score = get_total_score(assessment)
        if score < organization_score:
            number_below += 1
        elif score == organization_score:
            number_equal += 1

    rank = (number_below + 0.5 * number_equal) / total * 100
    return int(round(rank))

def calculate_dimension_comparison(your_scores: Dict[str, float], benchmark_averages: Dict[str, int]) -> Dict[str, Dict[str, Union[float, int]]]:
    comparisons = {}
    for dim, benchmark in benchmark_averages.items():
        if dim in your_scores:
            your_score = your_scores[dim]
            is_whole_number = isinstance(your_score, int) or (isinstance(your_score, float) and your_score.is_integer())
            comparisons[dim] = {
                "your_score": int(round(your_score)) if is_whole_number else your_score,
                "benchmark": benchmark,
                "difference": int(round(your_score)) - benchmark if is_whole_number else your_score - benchmark
            }
    return comparisons

def generate_benchmark_payload(organization_total_score: float, organization_dimension_scores: Dict[str, float], assessments: List[Any]) -> Dict[str, Any]:
    sample_size = len(assessments)
    validation_error = validate_sample_size(sample_size)
    if validation_error:
        return validation_error

    platform_average = calculate_platform_average(assessments)
    dimension_averages = calculate_dimension_averages(assessments)
    percentile_rank = calculate_percentile_rank(organization_total_score, assessments)
    dimension_comparisons = calculate_dimension_comparison(organization_dimension_scores, dimension_averages)

    return {
        "benchmark_available": True,
        "sample_size": sample_size,
        "platform_average": platform_average,
        "percentile_rank": percentile_rank,
        "dimension_comparisons": dimension_comparisons,
        "benchmark_summary": ""
    }
