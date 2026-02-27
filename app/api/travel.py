from fastapi import APIRouter
from app.Schemas.travel import TravelRequest
from app.agents.travel_agent import llm,agent_executor
from app.tools.flights import search_flights
from app.tools.hotels import search_hotels

router = APIRouter()

@router.get("/llm-test")
def llm_test():
    response = llm.invoke("Suggest a budget-friendly travel destination in December.")
    return {"response": response.content}

@router.post("/plan")
def plan_trip(request: TravelRequest):
    return {"message": "Input received", "data": request}

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

@router.post("/plan")
def plan_trip(request: TravelRequest):
    user_input = (
        f"Plan a trip from {request.origin_city} "
        f"with total budget {request.budget} "
        f"from {request.start_date} to {request.end_date}. "
        f"Preferences: {request.preferences}"
    )

    result = agent_executor.invoke({
        "messages": [("human", user_input)]
    })

    return {
        "plan": result["messages"][-1].content
    }