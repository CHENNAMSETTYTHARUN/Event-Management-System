from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.models.base import Base

class EventCategory(Base):
    __tablename__ = "event_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)

    events = relationship("Event", back_populates="category")
