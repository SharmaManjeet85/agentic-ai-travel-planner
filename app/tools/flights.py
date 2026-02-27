import os
import httpx
from langchain.tools import tool
from app.utils.logger import get_logger
from app.utils.date_utils import normalize_date
logger = get_logger("flights")

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
SKYSCANNER_HOST = os.getenv("SKYSCANNER_HOST")


@tool
def search_flights(
    origin: str,
    destination: str,
    start_date: str,
    end_date: str,
    budget: int
) -> str:
    """
    Search flights using Skyscanner RapidAPI.
    Dates are normalized internally.
    """

    try:
        start_date = normalize_date(start_date)
        end_date = normalize_date(end_date)
    except ValueError as e:
        logger.error(str(e))
        return "Invalid date format provided."

    logger.info(
        f"Searching flights {origin} → {destination} "
        f"{start_date} to {end_date}"
    )

    if not RAPIDAPI_KEY:
        logger.warning("RAPIDAPI_KEY missing. Using mock flights.")
        return _mock_flights(origin, destination, budget)

    url = "https://skyscanner44.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "skyscanner44.p.rapidapi.com",
    }

    params = {
        "adults": 1,
        "origin": origin,
        "destination": destination,
        "departureDate": start_date,   # ✅ ISO
        "returnDate": end_date,        # ✅ ISO
        "currency": "USD",
    }

    response = httpx.get(url, headers=headers, params=params, timeout=20)
    
    logger.info(f"Skyscanner response: {response.status_code}")

    if response.status_code == 404:
            logger.warning("Skyscanner unavailable. Falling back to mock flights.")
            return _mock_flights(origin, destination, budget)

    response.raise_for_status()
    data = response.json()

    return _parse_flights(data, budget)

def _parse_flights(data: dict, budget: int) -> str:
    """
    Parse Skyscanner search response and return readable flight options.
    """

    itineraries = (
        data.get("itineraries", {})
            .get("results", {})
    )

    if not itineraries:
        return "No flight itineraries found."

    results = []
    for _, item in itineraries.items():
        try:
            pricing = item["pricingOptions"][0]
            price = int(pricing["price"]["amount"])

            if price > budget:
                continue

            leg_ids = item.get("legIds", [])
            results.append(
                f"Flight option | Price: ${price} | Legs: {len(leg_ids)}"
            )

            if len(results) >= 5:
                break

        except (KeyError, IndexError, TypeError):
            # Skyscanner response shape is unstable
            continue
    
    if not results:
        return "No flights within budget."

    return "\n".join(results)

def _mock_flights(origin: str, destination: str, budget: int) -> str:
    options = [
        {"price": 420, "stops": 1, "carrier": "IndiGo"},
        {"price": 510, "stops": 0, "carrier": "Emirates"},
        {"price": 680, "stops": 1, "carrier": "Air India"},
    ]

    results = [
        f"{o['carrier']} | {origin} → {destination} | "
        f"${o['price']} | Stops: {o['stops']}"
        for o in options
        if o["price"] <= budget
    ]

    return "\n".join(results) if results else "No flights within budget."