from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.models.base import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey("event_categories.id"), nullable=False)
    organizer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    venue = Column(String(255), nullable=False)
    capacity = Column(Integer, nullable=False)
    status = Column(String(50), default="Draft", nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    category = relationship("EventCategory", back_populates="events")
    organizer = relationship("User", back_populates="organized_events")
    registrations = relationship("Registration", back_populates="event")
    attendances = relationship("Attendance", back_populates="event")
