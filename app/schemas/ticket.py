from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.registration import RegistrationResponse

class TicketBase(BaseModel):
    registration_id: int = Field(..., examples=[1])

class TicketGenerateRequest(TicketBase):
    pass

class TicketResponse(TicketBase):
    id: int
    ticket_number: str
    qr_code: str
    status: str
    created_at: datetime
    registration: Optional[RegistrationResponse] = None

    class Config:
        from_attributes = True

class TicketValidateRequest(BaseModel):
    ticket_number: str = Field(..., examples=["TICKET-1234567890"])
    event_id: int = Field(..., examples=[1])

class TicketValidationResponse(BaseModel):
    valid: bool
    message: str
    ticket: Optional[TicketResponse] = None
