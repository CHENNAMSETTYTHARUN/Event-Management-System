from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.models.event import Event
from app.repositories.base import BaseRepository

class EventRepository(BaseRepository[Event]):
    def __init__(self):
        super().__init__(Event)

    def get_filtered_events(
        self,
        db: Session,
        *,
        search: Optional[str] = None,
        category_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        status: Optional[str] = None,
        organizer_id: Optional[int] = None,
        sort_by: str = "start_date",
        sort_order: str = "asc",
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[Event], int]:
        query = db.query(Event)

        if search:
            query = query.filter(Event.name.ilike(f"%{search}%"))

        if category_id:
            query = query.filter(Event.category_id == category_id)

        if start_date:
            query = query.filter(Event.start_date >= start_date)

        if end_date:
            query = query.filter(Event.end_date <= end_date)

        if status:
            query = query.filter(Event.status == status)

        if organizer_id:
            query = query.filter(Event.organizer_id == organizer_id)

        total_count = query.count()

        sort_attr = getattr(Event, sort_by, None)
        if sort_attr is None:
            sort_attr = Event.start_date

        if sort_order.lower() == "desc":
            query = query.order_by(sort_attr.desc())
        else:
            query = query.order_by(sort_attr.asc())

        events = query.offset(skip).limit(limit).all()
        return events, total_count

event_repo = EventRepository()
