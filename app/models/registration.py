from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import relationship
from app.models.base import Base

class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    registration_date = Column(DateTime, server_default=func.now(), nullable=False)
    status = Column(String(50), default="Confirmed", nullable=False)

    event = relationship("Event", back_populates="registrations")
    user = relationship("User", back_populates="registrations")
    ticket = relationship("Ticket", back_populates="registration", uselist=False, cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("event_id", "user_id", name="uq_event_user_confirmed"),
    )
