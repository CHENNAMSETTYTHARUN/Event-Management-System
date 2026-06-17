from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, model_validator
from app.schemas.category import CategoryResponse
from app.schemas.user import UserResponse

class EventBase(BaseModel):
    name: str = Field(..., min_length=2, examples=["AI Conference 2026"])
    description: Optional[str] = Field(None, examples=["Annual global conference on artificial intelligence."])
    category_id: int = Field(..., examples=[1])
    start_date: datetime = Field(..., examples=["2026-07-20T09:00:00"])
    end_date: datetime = Field(..., examples=["2026-07-20T17:00:00"])
    venue: str = Field(..., examples=["Silicon Valley Convention Center"])
    capacity: int = Field(..., gt=0, examples=[500])
    status: str = Field("Draft", examples=["Published"])

class EventCreate(EventBase):
    @model_validator(mode="after")
    def validate_dates(self) -> "EventCreate":
        if self.start_date <= datetime.now():
            raise ValueError("Start date must be in the future")
        if self.end_date <= self.start_date:
            raise ValueError("End date must be after start date")
        return self

class EventUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, examples=["AI Conference 2026 - Updated"])
    description: Optional[str] = Field(None, examples=["Updated event description."])
    category_id: Optional[int] = Field(None, examples=[1])
    start_date: Optional[datetime] = Field(None, examples=["2026-07-20T10:00:00"])
    end_date: Optional[datetime] = Field(None, examples=["2026-07-20T18:00:00"])
    venue: Optional[str] = Field(None, examples=["Online Zoom Session"])
    capacity: Optional[int] = Field(None, gt=0, examples=[1000])
    status: Optional[str] = Field(None, examples=["Published"])

    @model_validator(mode="after")
    def validate_dates(self) -> "EventUpdate":
        if self.start_date and self.start_date <= datetime.now():
            raise ValueError("Start date must be in the future")
        if self.start_date and self.end_date and self.end_date <= self.start_date:
            raise ValueError("End date must be after start date")
        return self

class EventResponse(EventBase):
    id: int
    organizer_id: int
    created_at: datetime
    updated_at: datetime
    category: Optional[CategoryResponse] = None
    organizer: Optional[UserResponse] = None

    class Config:
        from_attributes = True

class EventListResponse(BaseModel):
    total: int
    events: List[EventResponse]
