from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.user import User
from app.schemas.report import EventReportResponse, RegistrationReportResponse, AttendanceReportResponse
from app.services.report import report_service

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/events", response_model=EventReportResponse)
def get_events_report(
    current_user: User = Depends(deps.RoleChecker(allowed_roles=["Organizer"])),
    db: Session = Depends(get_db)
):
    is_admin = current_user.role.name == "Admin"
    return report_service.get_event_report(db, user_id=current_user.id, is_admin=is_admin)

@router.get("/registrations", response_model=RegistrationReportResponse)
def get_registrations_report(
    current_user: User = Depends(deps.RoleChecker(allowed_roles=["Organizer"])),
    db: Session = Depends(get_db)
):
    is_admin = current_user.role.name == "Admin"
    return report_service.get_registration_report(db, user_id=current_user.id, is_admin=is_admin)

@router.get("/attendance/{event_id}", response_model=AttendanceReportResponse)
def get_attendance_report(
    event_id: int,
    current_user: User = Depends(deps.RoleChecker(allowed_roles=["Organizer"])),
    db: Session = Depends(get_db)
):
    is_admin = current_user.role.name == "Admin"
    return report_service.get_attendance_report(db, event_id=event_id, user_id=current_user.id, is_admin=is_admin)
