import pytest
from benchmarking.service import (
    get_total_score,
    get_dimension_scores,
    validate_sample_size,
    calculate_platform_average,
    calculate_dimension_averages,
    calculate_percentile_rank,
    calculate_dimension_comparison,
    generate_benchmark_payload
)

class MockSQLAlchemyAudit:
    def __init__(self, total_score, scores):
        self.total_score = total_score
        self.scores = scores

def test_get_total_score():
    assert get_total_score({"total_score": 60}) == 60.0
    assert get_total_score(MockSQLAlchemyAudit(60, {})) == 60.0
    assert get_total_score({}) == 0.0

def test_get_dimension_scores():
    dict_scores = {"awareness": 61, "adoption": 58}
    assert get_dimension_scores({"dimension_scores": dict_scores}) == {"awareness": 61.0, "adoption": 58.0}
    assert get_dimension_scores({"scores": dict_scores}) == {"awareness": 61.0, "adoption": 58.0}

    obj = MockSQLAlchemyAudit(60, dict_scores)
    assert get_dimension_scores(obj) == {"awareness": 61.0, "adoption": 58.0}

def test_validate_sample_size():
    assert validate_sample_size(9) == {
        "benchmark_available": False,
        "message": "Insufficient benchmark data available.",
        "sample_size": 9
    }
    assert validate_sample_size(10) is None

def test_calculate_platform_average():
    assessments = [
        {"total_score": 58},
        {"total_score": 59},
        {"total_score": 58}
    ]
    # (58 + 59 + 58) / 3 = 175 / 3 = 58.333... -> 58.3
    assert calculate_platform_average(assessments) == 58.3

def test_calculate_dimension_averages():
    assessments = [
        {"dimension_scores": {"awareness": 61, "adoption": 58}},
        {"dimension_scores": {"awareness": 60, "adoption": 60}},
        {"dimension_scores": {"awareness": 63, "adoption": 55}}
    ]
    # awareness: (61+60+63)/3 = 61.333 -> 61
    # adoption: (58+60+55)/3 = 57.666 -> 58
    assert calculate_dimension_averages(assessments) == {"awareness": 61, "adoption": 58}

def test_calculate_percentile_rank():
    # 10 assessments
    assessments = [{"total_score": i * 10} for i in range(1, 11)]
    # Scores: 10, 20, 30, 40, 50, 60, 70, 80, 90, 100

    # Org score 50.
    # below: 4 (10, 20, 30, 40)
    # equal: 1 (50)
    # rank = (4 + 0.5 * 1) / 10 * 100 = 4.5 / 10 * 100 = 45
    assert calculate_percentile_rank(50, assessments) == 45

    # Check for tied scores
    tied_assessments = [{"total_score": 50} for _ in range(10)]
    # Org score 50. below: 0, equal: 10
    # rank = (0 + 0.5 * 10) / 10 * 100 = 50
    assert calculate_percentile_rank(50, tied_assessments) == 50

def test_calculate_dimension_comparison():
    your_scores = {"awareness": 72.0, "adoption": 50.0}
    benchmarks = {"awareness": 61, "adoption": 58, "roi": 55}

    expected = {
        "awareness": {"your_score": 72, "benchmark": 61, "difference": 11},
        "adoption": {"your_score": 50, "benchmark": 58, "difference": -8}
    }

    assert calculate_dimension_comparison(your_scores, benchmarks) == expected

def test_generate_benchmark_payload_insufficient_sample():
    assessments = [{"total_score": 50}] * 5
    payload = generate_benchmark_payload(50, {}, assessments)
    assert payload["benchmark_available"] is False
    assert payload["message"] == "Insufficient benchmark data available."
    assert payload["sample_size"] == 5

def test_generate_benchmark_payload_success():
    assessments = [
        {"total_score": 60, "dimension_scores": {"awareness": 60, "adoption": 60}} for _ in range(10)
    ]

    your_scores = {"awareness": 70, "adoption": 50}
    payload = generate_benchmark_payload(65, your_scores, assessments)

    assert payload["benchmark_available"] is True
    assert payload["sample_size"] == 10
    assert payload["platform_average"] == 60.0

    # Rank: below: 10, equal: 0 -> (10 + 0) / 10 * 100 = 100
    assert payload["percentile_rank"] == 100

    assert payload["dimension_comparisons"] == {
        "awareness": {"your_score": 70, "benchmark": 60, "difference": 10},
        "adoption": {"your_score": 50, "benchmark": 60, "difference": -10}
    }
    assert "benchmark_insights" in payload
    assert payload["benchmark_insights"]["overall_summary"] == "Your organization performs above the current platform average by 5 points and ranks in the 100th percentile based on 10 completed assessments."
