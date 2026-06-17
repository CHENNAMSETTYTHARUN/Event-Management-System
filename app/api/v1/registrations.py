from typing import List
from fastapi import APIRouter, Depends, BackgroundTasks, status, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.user import User
from app.schemas.registration import RegistrationCreate, RegistrationResponse
from app.services.registration import registration_service

router = APIRouter(prefix="/registrations", tags=["Registrations"])

@router.post("", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
def register_event(
    request: RegistrationCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.RoleChecker(allowed_roles=["Participant"])),
    db: Session = Depends(get_db)
):
    return registration_service.register_for_event(
        db,
        user_id=current_user.id,
        request=request,
        background_tasks=background_tasks
    )

@router.put("/{registration_id}/cancel", response_model=RegistrationResponse)
def cancel_registration(
    registration_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    is_admin = current_user.role.name == "Admin"
    return registration_service.cancel_registration(
        db,
        registration_id=registration_id,
        user_id=current_user.id,
        is_admin=is_admin
    )

@router.get("/history", response_model=List[RegistrationResponse])
def registration_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(deps.RoleChecker(allowed_roles=["Participant"])),
    db: Session = Depends(get_db)
):
    return registration_service.get_user_history(db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/event/{event_id}", response_model=List[RegistrationResponse])
def view_event_registrations(
    event_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    is_admin = current_user.role.name == "Admin"
    return registration_service.get_event_registrations(
        db,
        event_id=event_id,
        user_id=current_user.id,
        is_admin=is_admin,
        skip=skip,
        limit=limit
    )
