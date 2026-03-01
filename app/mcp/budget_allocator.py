from typing import Dict

def allocate_budget(
    total_budget: int,
    flight_cost: float,
    hotel_cost_per_night: float,
    nights: int
) -> Dict:
    """
    MCP tool: deterministic budget validation & reasoning.
    """

    hotel_total = hotel_cost_per_night * nights
    total_cost = flight_cost + hotel_total

    return {
        "flight_budget_ok": flight_cost <= total_budget * 0.6,
        "hotel_budget_ok": hotel_total <= total_budget * 0.4,
        "total_cost": total_cost,
        "within_budget": total_cost <= total_budget,
        "recommendation": (
            "Budget is feasible"
            if total_cost <= total_budget
            else "Reduce hotel nights or choose cheaper options"
        )
    }