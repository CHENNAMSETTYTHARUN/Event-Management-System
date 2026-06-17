from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.models.base import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    registration_id = Column(Integer, ForeignKey("registrations.id"), unique=True, nullable=False)
    ticket_number = Column(String(100), unique=True, index=True, nullable=False)
    qr_code = Column(Text, nullable=False)
    status = Column(String(50), default="Active", nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    registration = relationship("Registration", back_populates="ticket")
