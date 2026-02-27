from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from app.utils.logger import get_logger
from app.api.travel import router as travel_router

load_dotenv()

logger = get_logger("startup")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Travel Planner API starting up")
    yield
    logger.info("Travel Planner API shutting down")


app = FastAPI(
    title="Agentic AI Travel Planner",
    lifespan=lifespan
)

app.include_router(travel_router, prefix="/api")


@app.get("/health")
def health_check():
    return {"status": "ok"}