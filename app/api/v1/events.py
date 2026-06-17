from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.user import User
from app.schemas.event import EventCreate, EventUpdate, EventResponse, EventListResponse
from app.services.event import event_service

router = APIRouter(prefix="/events", tags=["Events"])

@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
    request: EventCreate,
    current_user: User = Depends(deps.RoleChecker(allowed_roles=["Organizer"])),
    db: Session = Depends(get_db)
):
    return event_service.create_event(db, current_user.id, request)

@router.get("", response_model=EventListResponse)
def list_events(
    search: Optional[str] = Query(None, description="Search by event name"),
    category_id: Optional[int] = Query(None, description="Filter by category"),
    start_date: Optional[datetime] = Query(None, description="Filter start date from"),
    end_date: Optional[datetime] = Query(None, description="Filter end date to"),
    status: Optional[str] = Query(None, description="Filter by event status"),
    organizer_id: Optional[int] = Query(None, description="Filter by organizer id"),
    sort_by: str = Query("start_date", description="Sort by attribute"),
    sort_order: str = Query("asc", description="Sort direction: asc or desc"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    events, total = event_service.list_events(
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
    return {"total": total, "events": events}

@router.get("/{event_id}", response_model=EventResponse)
def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    return event_service.get_event(db, event_id)

@router.put("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: int,
    request: EventUpdate,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    is_admin = current_user.role.name == "Admin"
    return event_service.update_event(
        db,
        event_id=event_id,
        user_id=current_user.id,
        is_admin=is_admin,
        request=request
    )

@router.delete("/{event_id}", response_model=EventResponse)
def delete_event(
    event_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    is_admin = current_user.role.name == "Admin"
    return event_service.delete_event(
        db,
        event_id=event_id,
        user_id=current_user.id,
        is_admin=is_admin
    )
