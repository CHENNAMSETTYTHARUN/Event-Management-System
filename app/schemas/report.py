from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class EventReportItem(BaseModel):
    event_id: int
    event_name: str
    start_date: datetime
    end_date: datetime
    capacity: int
    status: str
    total_registrations: int
    attendance_rate: float

class RegistrationReportItem(BaseModel):
    registration_id: int
    event_name: str
    participant_name: str
    participant_email: str
    registration_date: datetime
    status: str

class AttendanceReportItem(BaseModel):
    user_id: int
    full_name: str
    email: str
    attendance_status: str
    check_in_time: Optional[datetime] = None

class EventReportResponse(BaseModel):
    generated_at: datetime
    events: List[EventReportItem]

class RegistrationReportResponse(BaseModel):
    generated_at: datetime
    registrations: List[RegistrationReportItem]

class AttendanceReportResponse(BaseModel):
    generated_at: datetime
    event_id: int
    event_name: str
    attendance: List[AttendanceReportItem]
