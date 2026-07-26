from typing import List, Dict, Any, Union
from pydantic import BaseModel

class SystemData(BaseModel):
    id: str = ""
    licensing_cost: float | None = None
    cloud_cost: float | None = None
    inference_cost: float | None = None
    maintenance_cost: float | None = None
    criticality: str | None = None

def _get_cost_value(val: float | None) -> float | None:
    if val is None:
        return None
    return float(val)

def calculate_system_cost(system: Union[BaseModel, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculates the total cost for a single AI system based on its granular cost fields.
    Gracefully handles NULLs by marking the result as partial if any cost field is missing.
    If all fields are NULL, total is 0.0, is_partial=True, missing_components=all.
    """
    if isinstance(system, dict):
        licensing = _get_cost_value(system.get("licensing_cost"))
        cloud = _get_cost_value(system.get("cloud_cost"))
        inference = _get_cost_value(system.get("inference_cost"))
        maintenance = _get_cost_value(system.get("maintenance_cost"))
    else:
        licensing = _get_cost_value(getattr(system, "licensing_cost", None))
        cloud = _get_cost_value(getattr(system, "cloud_cost", None))
        inference = _get_cost_value(getattr(system, "inference_cost", None))
        maintenance = _get_cost_value(getattr(system, "maintenance_cost", None))

    missing_components = []
    total = 0.0

    if licensing is not None:
        total += licensing
    else:
        missing_components.append("licensing_cost")

    if cloud is not None:
        total += cloud
    else:
        missing_components.append("cloud_cost")

    if inference is not None:
        total += inference
    else:
        missing_components.append("inference_cost")

    if maintenance is not None:
        total += maintenance
    else:
        missing_components.append("maintenance_cost")

    is_partial = len(missing_components) > 0

    return {
        "total": total,
        "is_partial": is_partial,
        "missing_components": missing_components
    }

def calculate_org_cost(systems: List[Union[BaseModel, Dict[str, Any]]]) -> Dict[str, Any]:
    """
    Calculates the org-level rollup cost across a list of AI systems.
    If any system has partial cost data, the org-level rollup is also marked as partial.
    If no systems have data, or if the system list is empty, returns gracefully.
    """
    total = 0.0
    systems_with_data = 0
    total_systems = len(systems)
    is_partial = False

    for system in systems:
        system_calc = calculate_system_cost(system)
        if not system_calc["is_partial"]:
            systems_with_data += 1
        elif system_calc["total"] > 0:
            systems_with_data += 1
            is_partial = True
        else:
            is_partial = True

        total += system_calc["total"]

    return {
        "total": total,
        "is_partial": is_partial,
        "systems_with_data": systems_with_data,
        "total_systems": total_systems
    }

def calculate_cost_by_criticality(systems: List[Union[BaseModel, Dict[str, Any]]]) -> Dict[str, Dict[str, Any]]:
    """
    Groups systems by criticality and calculates the rollup cost for each tier.
    """
    grouped_systems: Dict[str, List[Any]] = {}

    for system in systems:
        if isinstance(system, dict):
            criticality = system.get("criticality") or "Unknown"
        else:
            criticality = getattr(system, "criticality", None) or "Unknown"

        if criticality not in grouped_systems:
            grouped_systems[criticality] = []
        grouped_systems[criticality].append(system)

    result = {}
    for crit, sys_list in grouped_systems.items():
        result[crit] = calculate_org_cost(sys_list)

    return result
