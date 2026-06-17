from datetime import datetime
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException, ForbiddenException
from app.models.event import Event
from app.models.registration import Registration
from app.models.attendance import Attendance
from app.repositories.event import event_repo

class ReportService:
    @staticmethod
    def get_event_report(db: Session, user_id: int, is_admin: bool) -> dict:
        query = db.query(Event)
        if not is_admin:
            query = query.filter(Event.organizer_id == user_id)

        events = query.all()
        report_items = []

        for event in events:
            total_reg = db.query(Registration).filter(
                Registration.event_id == event.id,
                Registration.status == "Confirmed"
            ).count()

            attendances = db.query(Attendance).filter(Attendance.event_id == event.id).all()
            total_present = sum(1 for a in attendances if a.attendance_status.lower() == "present")

            rate = (total_present / total_reg * 100) if total_reg > 0 else 0.0

            report_items.append({
                "event_id": event.id,
                "event_name": event.name,
                "start_date": event.start_date,
                "end_date": event.end_date,
                "capacity": event.capacity,
                "status": event.status,
                "total_registrations": total_reg,
                "attendance_rate": round(rate, 2)
            })

        return {
            "generated_at": datetime.now(),
            "events": report_items
        }

    @staticmethod
    def get_registration_report(db: Session, user_id: int, is_admin: bool) -> dict:
        query = db.query(Registration)
        if not is_admin:
            query = query.join(Event).filter(Event.organizer_id == user_id)

        registrations = query.order_by(Registration.registration_date.desc()).all()
        report_items = []

        for reg in registrations:
            report_items.append({
                "registration_id": reg.id,
                "event_name": reg.event.name,
                "participant_name": reg.user.full_name,
                "participant_email": reg.user.email,
                "registration_date": reg.registration_date,
                "status": reg.status
            })

        return {
            "generated_at": datetime.now(),
            "registrations": report_items
        }

    @staticmethod
    def get_attendance_report(db: Session, event_id: int, user_id: int, is_admin: bool) -> dict:
        event = event_repo.get(db, event_id)
        if not event:
            raise NotFoundException("Event not found")

        if not is_admin and event.organizer_id != user_id:
            raise ForbiddenException("You do not have permission to view reports for this event")

        registrations = db.query(Registration).filter(
            Registration.event_id == event_id,
            Registration.status == "Confirmed"
        ).all()

        report_items = []
        for reg in registrations:
            att = db.query(Attendance).filter(
                Attendance.event_id == event_id,
                Attendance.user_id == reg.user_id
            ).first()

            report_items.append({
                "user_id": reg.user_id,
                "full_name": reg.user.full_name,
                "email": reg.user.email,
                "attendance_status": att.attendance_status if att else "Registered",
                "check_in_time": att.check_in_time if att else None
            })

        return {
            "generated_at": datetime.now(),
            "event_id": event_id,
            "event_name": event.name,
            "attendance": report_items
        }

report_service = ReportService()
