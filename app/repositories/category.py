from typing import Optional
from sqlalchemy.orm import Session
from app.models.category import EventCategory
from app.repositories.base import BaseRepository

class EventCategoryRepository(BaseRepository[EventCategory]):
    def __init__(self):
        super().__init__(EventCategory)

    def get_by_name(self, db: Session, name: str) -> Optional[EventCategory]:
        return db.query(EventCategory).filter(EventCategory.name == name).first()

category_repo = EventCategoryRepository()
