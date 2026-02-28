from fastapi import APIRouter
from app.Schemas.travel import TravelRequest
from app.agents.travel_agent import llm,agent_executor
from app.tools.flights import search_flights
from app.tools.hotels import search_hotels

router = APIRouter()

SYSTEM_PROMPT = """
You are a travel planning agent.

You will ALWAYS receive:
- origin city
- destination city
- start date
- end date
- total budget

Rules:
1. DO NOT ask follow-up questions.
2. DO NOT ask for clarification.
3. Assume the budget covers flights + hotels.
4. Always:
   - Check weather
   - Search flights
   - Search hotels
5. If data is missing or a tool fails:
   - Make a reasonable assumption
   - Clearly state the assumption in the response

Produce a final travel plan.
"""
@router.get("/llm-test")
def llm_test():
    response = llm.invoke("Suggest a budget-friendly travel destination in December.")
    return {"response": response.content}

@router.get("/test/flights")
def test_flights():
    return {
        "result": search_flights.invoke({
            "origin": "DEL",
            "destination": "DXB",
            "start_date": "15/04/2026",
            "end_date": "22/04/2026",
            "budget": 500
        })
    }
@router.get("/test/hotels")
def hotel_search(
    city: str,
    checkin_date: str,
    checkout_date: str,
    budget_per_night: int
):
    """
    Test hotel search endpoint (mock).
    """
    result = search_hotels.invoke({
        "city": "Del",
        "checkin_date": "15/04/2026",
        "checkout_date": "16/04/2026",
        "budget_per_night": 5000
    })

    return {"results": result}
def normalize_city(city: str) -> str:
    return city.strip().upper()

@router.post("/plan")
def plan_trip(req: TravelRequest):
    origin = normalize_city(req.origin_city)
    destination = normalize_city(req.destination_city)
    agent_input = f"""
    Plan a trip with the following details:

    Origin: {origin}
    Destination: {destination}
    Dates: {req.start_date} to {req.end_date}
    Budget: ${req.budget}
    Preferences: {req.preferences or "none"}

    Proceed with planning.
    """
    result = agent_executor.invoke({
        "messages": [
            ("system", SYSTEM_PROMPT),
            ("human", agent_input)
        ]
    })
    print(result["messages"][-1].content)
    return result["messages"][-1].content

