from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.user import User
from app.schemas.attendance import AttendanceMarkRequest, AttendanceResponse, AttendanceSummaryResponse
from app.services.attendance import attendance_service

router = APIRouter(prefix="/attendance", tags=["Attendance"])

@router.post("/mark", response_model=AttendanceResponse, status_code=status.HTTP_200_OK)
def mark_attendance(
    request: AttendanceMarkRequest,
    current_user: User = Depends(deps.RoleChecker(allowed_roles=["Organizer"])),
    db: Session = Depends(get_db)
):
    is_admin = current_user.role.name == "Admin"
    return attendance_service.mark_attendance(
        db,
        request=request,
        organizer_id=current_user.id,
        is_admin=is_admin
    )

@router.get("/event/{event_id}", response_model=List[AttendanceResponse])
def view_event_attendance(
    event_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    is_admin = current_user.role.name == "Admin"
    return attendance_service.get_event_attendance(
        db,
        event_id=event_id,
        user_id=current_user.id,
        is_admin=is_admin
    )

@router.get("/user/{user_id}", response_model=List[AttendanceResponse])
def view_user_attendance(
    user_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    is_admin = current_user.role.name == "Admin"
    return attendance_service.get_user_attendance(
        db,
        target_user_id=user_id,
        request_user_id=current_user.id,
        is_admin=is_admin
    )

@router.get("/summary/{event_id}", response_model=AttendanceSummaryResponse)
def get_attendance_summary(
    event_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    is_admin = current_user.role.name == "Admin"
    return attendance_service.get_attendance_summary(
        db,
        event_id=event_id,
        user_id=current_user.id,
        is_admin=is_admin
    )
