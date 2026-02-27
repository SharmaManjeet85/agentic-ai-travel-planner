from fastapi import APIRouter
from app.Schemas.travel import TravelRequest
from app.agents.travel_agent import llm

router = APIRouter()

@router.get("/llm-test")
def llm_test():
    response = llm.invoke("Suggest a budget-friendly travel destination in December.")
    return {"response": response.content}

@router.post("/plan")
def plan_trip(request: TravelRequest):
    return {"message": "Input received", "data": request}