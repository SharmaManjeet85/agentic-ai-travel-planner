from langchain.tools import tool
from app.mcp.budget_allocator import allocate_budget

@tool
def budget_mcp(
    total_budget: int,
    flight_cost: float,
    hotel_cost_per_night: float,
    nights: int
) -> dict:
    """
    Deterministic budget analysis using MCP logic.
    """
    return allocate_budget(
        total_budget,
        flight_cost,
        hotel_cost_per_night,
        nights
    )