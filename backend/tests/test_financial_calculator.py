import pytest
from financial.calculator import calculate_system_cost, calculate_org_cost, calculate_cost_by_criticality

class MockSystem:
    def __init__(self, lic=None, clo=None, inf=None, main=None, crit=None):
        self.licensing_cost = lic
        self.cloud_cost = clo
        self.inference_cost = inf
        self.maintenance_cost = main
        self.criticality = crit

def test_calculate_system_cost_all_nulls():
    system = MockSystem()
    result = calculate_system_cost(system)
    assert result["total"] == 0.0
    assert result["is_partial"] is True
    assert set(result["missing_components"]) == {"licensing_cost", "cloud_cost", "inference_cost", "maintenance_cost"}

def test_calculate_system_cost_partial_data():
    system = {"licensing_cost": 1000.0, "maintenance_cost": 500.0}
    result = calculate_system_cost(system)
    assert result["total"] == 1500.0
    assert result["is_partial"] is True
    assert set(result["missing_components"]) == {"cloud_cost", "inference_cost"}

def test_calculate_system_cost_full_data():
    system = MockSystem(lic=100.0, clo=200.0, inf=300.0, main=400.0)
    result = calculate_system_cost(system)
    assert result["total"] == 1000.0
    assert result["is_partial"] is False
    assert len(result["missing_components"]) == 0

def test_calculate_org_cost_mixed_systems():
    sys1 = MockSystem(lic=100.0, clo=200.0, inf=300.0, main=400.0) # Full, total 1000
    sys2 = MockSystem(lic=1000.0) # Partial, total 1000
    sys3 = MockSystem() # Zero/null

    result = calculate_org_cost([sys1, sys2, sys3])

    assert result["total"] == 2000.0
    assert result["is_partial"] is True
    assert result["systems_with_data"] == 2
    assert result["total_systems"] == 3

def test_calculate_org_cost_all_fully_costed():
    sys1 = MockSystem(lic=10.0, clo=10.0, inf=10.0, main=10.0)
    sys2 = MockSystem(lic=20.0, clo=20.0, inf=20.0, main=20.0)

    result = calculate_org_cost([sys1, sys2])

    assert result["total"] == 120.0
    assert result["is_partial"] is False
    assert result["systems_with_data"] == 2
    assert result["total_systems"] == 2

def test_calculate_cost_by_criticality():
    sys1 = MockSystem(lic=10.0, clo=10.0, inf=10.0, main=10.0, crit="High")
    sys2 = MockSystem(lic=10.0, crit="High")
    sys3 = MockSystem(lic=50.0, clo=50.0, inf=50.0, main=50.0, crit="Low")
    sys4 = MockSystem(crit="Medium") # null

    result = calculate_cost_by_criticality([sys1, sys2, sys3, sys4])

    assert "High" in result
    assert result["High"]["total"] == 50.0
    assert result["High"]["is_partial"] is True
    assert result["High"]["systems_with_data"] == 2

    assert "Low" in result
    assert result["Low"]["total"] == 200.0
    assert result["Low"]["is_partial"] is False
    assert result["Low"]["systems_with_data"] == 1

    assert "Medium" in result
    assert result["Medium"]["total"] == 0.0
    assert result["Medium"]["is_partial"] is True
    assert result["Medium"]["systems_with_data"] == 0

    assert result["High"]["total_systems"] == 2
    assert result["Low"]["total_systems"] == 1
    assert result["Medium"]["total_systems"] == 1
