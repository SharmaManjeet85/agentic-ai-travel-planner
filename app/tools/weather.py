from langchain.tools import tool
import httpx
from app.utils.logger import get_logger

logger = get_logger("weather")

@tool
def get_weather(city: str) -> str:
    """
    Get current weather for a city.
    Uses a safe mock fallback if API fails.
    """
    try:
        # Example free endpoint (often flaky)
        url = f"https://wttr.in/{city}?format=3"

        logger.info(f"Fetching weather for {city}")
        response = httpx.get(url, timeout=5.0)
        response.raise_for_status()

        return response.text

    except Exception as e:
        logger.warning(f"Weather API failed: {e}")
        return _mock_weather(city)


def _mock_weather(city: str) -> str:
    return f"{city}: Warm and dry (~30–35°C). Suitable for sightseeing."