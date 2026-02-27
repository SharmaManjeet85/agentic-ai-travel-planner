import os
import httpx
from langchain.tools import tool

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")


@tool
def search_hotels(
    city: str,
    checkin_date: str,
    checkout_date: str,
    budget_per_night: int
) -> str:
    """
    Search hotels using Booking.com Rapid API (free tier).
    Falls back to mock data if API fails.
    Dates format: YYYY-MM-DD
    """

    if not RAPIDAPI_KEY:
        return _mock_hotels(city, budget_per_night)

    url = "https://booking-com.p.rapidapi.com/v1/hotels/search"

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST,
    }

    params = {
        "checkout_date": checkout_date,
        "checkin_date": checkin_date,
        "units": "metric",
        "order_by": "price",
        "adults_number": 2,
        "room_number": 1,
        "filter_by_currency": "USD",
        "dest_type": "city",
        "dest_id": city,
        "price_max": budget_per_night,
        "locale": "en-us",
    }

    try:
        response = httpx.get(url, headers=headers, params=params, timeout=20)
        response.raise_for_status()
        hotels = response.json().get("result", [])[:3]

        if not hotels:
            return "No hotels found within budget."

        results = []
        for h in hotels:
            results.append(
                f"{h.get('hotel_name')} | "
                f"${h.get('min_total_price', 'N/A')}/night | "
                f"⭐ {h.get('review_score', 'N/A')}"
            )

        return "\n".join(results)

    except Exception:
        return _mock_hotels(city, budget_per_night)


def _mock_hotels(city: str, budget: int) -> str:
    """Fallback mock hotels"""
    return "\n".join([
        f"City Comfort Inn ({city}) | ${budget - 20}/night | ⭐ 4.2",
        f"Urban Stay ({city}) | ${budget - 30}/night | ⭐ 4.0",
        f"Budget Lodge ({city}) | ${budget - 40}/night | ⭐ 3.8",
    ])