from fastapi import FastAPI
from app.api.travel import router as travel_router

app = FastAPI(title="Agentic AI Travel Planner")
app.include_router(travel_router, prefix="/api")


@app.get("/health")
def health_check():
    return {"status": "ok"}