from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.event import EventResponse
from app.schemas.user import UserResponse

class RegistrationBase(BaseModel):
    event_id: int = Field(..., examples=[1])

class RegistrationCreate(RegistrationBase):
    pass

class RegistrationResponse(RegistrationBase):
    id: int
    user_id: int
    registration_date: datetime
    status: str
    event: Optional[EventResponse] = None
    user: Optional[UserResponse] = None

    class Config:
        from_attributes = True
