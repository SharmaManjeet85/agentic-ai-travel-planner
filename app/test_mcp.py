from app.mcp.budget_allocator import allocate_budget

result = allocate_budget(
    total_budget=500,
    flight_cost=320,
    hotel_cost_per_night=60,
    nights=5
)

print(result)