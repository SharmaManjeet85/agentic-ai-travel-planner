from pydantic import BaseModel
from typing import Literal, Dict, Any

MemoryType = Literal[
    "user_preference",
    "past_trip",
    "rejection_reason",
    "accepted_plan"
]

class MemoryRecord(BaseModel):
    type: MemoryType
    content: str
    metadata: Dict[str, Any]