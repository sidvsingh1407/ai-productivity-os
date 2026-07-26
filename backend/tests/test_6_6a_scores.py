import pytest
from adoption.scoring import calculate_adoption_score
from data_intelligence.scoring import calculate_data_score
from financial.scoring import calculate_roi_score

def test_adoption_score():
    # 1. High Score Scenario (100 users = 100 points, daily use = 1.2x, no shadow, completed training = +20 -> clamped to 100)
    high_record = {
        "user_count": 120,
        "usage_frequency": "daily",
        "shadow_ai_detected": False,
        "resistance_level": "low",
        "training_status": "completed"
    }
    assert calculate_adoption_score(high_record) == 100.0

    # 2. Medium Score Scenario (20 users = 50 points, weekly = 1.0x, medium resistance = -15 -> 35 points)
    medium_record = {
        "user_count": 20,
        "usage_frequency": "weekly",
        "shadow_ai_detected": False,
        "resistance_level": "medium",
        "training_status": "none"
    }
    assert calculate_adoption_score(medium_record) == 35.0

    # 3. Low/Penalized Score Scenario (5 users = 25 points, rare = 0.5x = 12.5 points, shadow AI = -20 -> clamped to 0)
    low_record = {
        "user_count": 5,
        "usage_frequency": "rare",
        "shadow_ai_detected": True,
        "resistance_level": "high",
        "training_status": "none"
    }
    assert calculate_adoption_score(low_record) == 0.0

def test_data_score():
    # 1. High Score Scenario (base 100, medium sensitivity (no penalty), real_time freshness (no penalty), owner present (no penalty))
    high_system = {
        "data_sensitivity": "medium",
        "data_freshness": "real_time",
        "data_owner": "user@example.com"
    }
    assert calculate_data_score(high_system) == 100.0

    # 2. Medium Score Scenario (base 100, stale data (-20), owner missing (-15), total 65)
    medium_system = {
        "data_sensitivity": "low",
        "data_freshness": "stale",
        "data_owner": None
    }
    assert calculate_data_score(medium_system) == 65.0

    # 3. Low/Penalized Score Scenario (base 100, high sensitivity with public access (-25), static freshness (-20), owner missing (-15), total 40)
    low_system = {
        "data_sensitivity": "high",
        "data_accessibility": ["public"],
        "data_freshness": "static",
        "data_owner": ""
    }
    assert calculate_data_score(low_system) == 40.0

def test_roi_score_structural_output():
    # 1. Full cost data
    system_full_cost = {
        "licensing_cost": 1000,
        "cloud_cost": 500,
        "inference_cost": 200,
        "maintenance_cost": 100,
        "expected_benefits": "Save a lot of time"
    }
    result_full = calculate_roi_score(system_full_cost)
    assert result_full["roi_score"] is None
    assert result_full["roi_score_unavailable_reason"] == "expected_benefits is not a structured numeric field"
    assert result_full["cost_is_partial"] is False
    assert result_full["cost_missing_components"] == []

    # 2. Partial cost data
    system_partial_cost = {
        "licensing_cost": 1000,
        "cloud_cost": None,
        "inference_cost": 200,
        "maintenance_cost": None,
        "expected_benefits": "Saves 10 hours a week"
    }
    result_partial = calculate_roi_score(system_partial_cost)
    assert result_partial["roi_score"] is None
    assert result_partial["roi_score_unavailable_reason"] == "expected_benefits is not a structured numeric field"
    assert result_partial["cost_is_partial"] is True
    assert "cloud_cost" in result_partial["cost_missing_components"]
    assert "maintenance_cost" in result_partial["cost_missing_components"]
