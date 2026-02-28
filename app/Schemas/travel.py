from pydantic import BaseModel
from typing import Optional

class TravelRequest(BaseModel):
    budget: int
    origin_city: str
    destination_city: str          # ✅ REQUIRED
    start_date: str
    end_date: str
    preferences: Optional[str] = None
    budget_scope: str = "flights+hotels"  # ✅ DEFAULT