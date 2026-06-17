from typing import List
from pydantic import BaseModel, Field

class EventRegistrationCount(BaseModel):
    event_id: int
    event_name: str
    registration_count: int

class DashboardResponse(BaseModel):
    total_events: int = Field(..., examples=[10])
    total_participants: int = Field(..., examples=[250])
    upcoming_events_count: int = Field(..., examples=[4])
    completed_events_count: int = Field(..., examples=[6])
    event_wise_registration_count: List[EventRegistrationCount] = Field(default=[])
