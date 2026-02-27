import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST= os.getenv("RAPIDAPI_HOST")
SKYSCANNER_HOST = os.getenv("SKYSCANNER_HOST")
