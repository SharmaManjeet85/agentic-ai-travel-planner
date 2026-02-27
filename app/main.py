from fastapi import FastAPI

app = FastAPI(title="Agentic AI Travel Planner")

@app.get("/health")
def health_check():
    return {"status": "ok"}