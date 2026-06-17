from datetime import datetime
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException, BadRequestException, ForbiddenException
from app.models.attendance import Attendance
from app.repositories.attendance import attendance_repo
from app.repositories.registration import registration_repo
from app.repositories.event import event_repo
from app.repositories.user import user_repo
from app.schemas.attendance import AttendanceMarkRequest
from app.services.audit_log import audit_log_service

class AttendanceService:
    @staticmethod
    def mark_attendance(
        db: Session,
        request: AttendanceMarkRequest,
        organizer_id: int,
        is_admin: bool
    ) -> Attendance:
        event = event_repo.get(db, request.event_id)
        if not event:
            raise NotFoundException("Event not found")

        if not is_admin and event.organizer_id != organizer_id:
            raise ForbiddenException("Only the event organizer or Admin can mark attendance")

        user = user_repo.get(db, request.user_id)
        if not user:
            raise NotFoundException("User not found")

        registration = registration_repo.get_by_event_and_user(db, event_id=request.event_id, user_id=request.user_id)
        if not registration or registration.status != "Confirmed":
            raise BadRequestException("Cannot mark attendance for a user who is not registered for this event")

        existing = attendance_repo.get_by_event_and_user(db, event_id=request.event_id, user_id=request.user_id)

        check_in = datetime.now() if request.attendance_status.lower() == "present" else None

        if existing:
            updated = attendance_repo.update(
                db,
                db_obj=existing,
                obj_in={
                    "attendance_status": request.attendance_status,
                    "check_in_time": check_in
                }
            )
            if request.attendance_status.lower() == "present" and registration.ticket:
                from app.repositories.ticket import ticket_repo
                ticket_repo.update(db, db_obj=registration.ticket, obj_in={"status": "Used"})

            audit_log_service.log_action(db, action="Mark Attendance", details={"event_id": request.event_id, "user_id": request.user_id, "status": request.attendance_status}, user_id=organizer_id)
            return updated

        attendance_obj = {
            "event_id": request.event_id,
            "user_id": request.user_id,
            "attendance_status": request.attendance_status,
            "check_in_time": check_in
        }

        attendance = attendance_repo.create(db, obj_in=attendance_obj)

        if request.attendance_status.lower() == "present" and registration.ticket:
            from app.repositories.ticket import ticket_repo
            ticket_repo.update(db, db_obj=registration.ticket, obj_in={"status": "Used"})

        audit_log_service.log_action(db, action="Mark Attendance", details={"event_id": request.event_id, "user_id": request.user_id, "status": request.attendance_status}, user_id=organizer_id)
        return attendance

    @staticmethod
    def get_event_attendance(db: Session, event_id: int, user_id: int, is_admin: bool):
        event = event_repo.get(db, event_id)
        if not event:
            raise NotFoundException("Event not found")

        if not is_admin and event.organizer_id != user_id:
            raise ForbiddenException("You do not have permission to view attendance for this event")

        return attendance_repo.get_event_attendance(db, event_id=event_id)

    @staticmethod
    def get_user_attendance(db: Session, target_user_id: int, request_user_id: int, is_admin: bool):
        if not is_admin and target_user_id != request_user_id:
            raise ForbiddenException("You do not have permission to view this user's attendance")

        return attendance_repo.get_user_attendance(db, user_id=target_user_id)

    @staticmethod
    def get_attendance_summary(db: Session, event_id: int, user_id: int, is_admin: bool) -> dict:
        event = event_repo.get(db, event_id)
        if not event:
            raise NotFoundException("Event not found")

        if not is_admin and event.organizer_id != user_id:
            raise ForbiddenException("You do not have permission to view attendance summary for this event")

        total_registered = registration_repo.get_active_count_by_event(db, event_id)

        attendances = attendance_repo.get_event_attendance(db, event_id)
        total_present = sum(1 for a in attendances if a.attendance_status.lower() == "present")
        total_absent = sum(1 for a in attendances if a.attendance_status.lower() == "absent")

        attendance_rate = (total_present / total_registered * 100) if total_registered > 0 else 0.0

        return {
            "event_id": event_id,
            "total_registered": total_registered,
            "total_present": total_present,
            "total_absent": total_absent,
            "attendance_rate": round(attendance_rate, 2)
        }

attendance_service = AttendanceService()
