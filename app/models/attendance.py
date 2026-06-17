from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    check_in_time = Column(DateTime, nullable=True)
    attendance_status = Column(String(50), default="Registered", nullable=False)

    event = relationship("Event", back_populates="attendances")
    user = relationship("User", back_populates="attendances")

    __table_args__ = (
        UniqueConstraint("event_id", "user_id", name="uq_event_user_attendance"),
    )
