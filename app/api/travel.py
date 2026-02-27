from fastapi import APIRouter
from app.agents.travel_agent import llm

router = APIRouter()

@router.get("/llm-test")
def llm_test():
    response = llm.invoke("Suggest a budget-friendly travel destination in December.")
    return {"response": response.content}