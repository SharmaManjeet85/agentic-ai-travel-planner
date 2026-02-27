import httpx
from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    url = f"https://wttr.in/{city}?format=3"
    return httpx.get(url).text