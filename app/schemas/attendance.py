from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.schemas.event import EventResponse
from app.schemas.user import UserResponse

class AttendanceBase(BaseModel):
    event_id: int = Field(..., examples=[1])
    user_id: int = Field(..., examples=[3])

class AttendanceMarkRequest(AttendanceBase):
    attendance_status: str = Field("Present", description="Present, Absent, etc.", examples=["Present"])

class AttendanceResponse(AttendanceBase):
    id: int
    check_in_time: Optional[datetime] = None
    attendance_status: str
    event: Optional[EventResponse] = None
    user: Optional[UserResponse] = None

    class Config:
        from_attributes = True

class AttendanceSummaryResponse(BaseModel):
    event_id: int
    total_registered: int
    total_present: int
    total_absent: int
    attendance_rate: float
