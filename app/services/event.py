from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException, ForbiddenException, BadRequestException
from app.models.event import Event
from app.repositories.event import event_repo
from app.repositories.category import category_repo
from app.schemas.event import EventCreate, EventUpdate
from app.services.audit_log import audit_log_service

class EventService:
    @staticmethod
    def create_event(db: Session, organizer_id: int, request: EventCreate) -> Event:
        category = category_repo.get(db, request.category_id)
        if not category:
            raise BadRequestException("Invalid category ID")

        event_data = request.model_dump()
        event_data["organizer_id"] = organizer_id

        event = event_repo.create(db, obj_in=event_data)

        audit_log_service.log_action(db, action="Create Event", details={"event_id": event.id, "name": event.name}, user_id=organizer_id)
        return event

    @staticmethod
    def get_event(db: Session, event_id: int) -> Event:
        event = event_repo.get(db, event_id)
        if not event:
            raise NotFoundException("Event not found")
        return event

    @staticmethod
    def list_events(
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
        return event_repo.get_filtered_events(
            db,
            search=search,
            category_id=category_id,
            start_date=start_date,
            end_date=end_date,
            status=status,
            organizer_id=organizer_id,
            sort_by=sort_by,
            sort_order=sort_order,
            skip=skip,
            limit=limit
        )

    @staticmethod
    def update_event(db: Session, event_id: int, user_id: int, is_admin: bool, request: EventUpdate) -> Event:
        event = event_repo.get(db, event_id)
        if not event:
            raise NotFoundException("Event not found")

        if not is_admin and event.organizer_id != user_id:
            raise ForbiddenException("You do not have permission to update this event")

        if request.category_id:
            category = category_repo.get(db, request.category_id)
            if not category:
                raise BadRequestException("Invalid category ID")

        updated_event = event_repo.update(db, db_obj=event, obj_in=request.model_dump(exclude_unset=True))

        audit_log_service.log_action(db, action="Update Event", details={"event_id": event_id}, user_id=user_id)
        return updated_event

    @staticmethod
    def delete_event(db: Session, event_id: int, user_id: int, is_admin: bool) -> Event:
        event = event_repo.get(db, event_id)
        if not event:
            raise NotFoundException("Event not found")

        if not is_admin and event.organizer_id != user_id:
            raise ForbiddenException("You do not have permission to delete this event")

        deleted_event = event_repo.remove(db, id=event_id)

        audit_log_service.log_action(db, action="Delete Event", details={"event_id": event_id}, user_id=user_id)
        return deleted_event

event_service = EventService()
