from datetime import datetime
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException, ConflictException, BadRequestException, ForbiddenException
from app.models.registration import Registration
from app.repositories.registration import registration_repo
from app.repositories.event import event_repo
from app.repositories.user import user_repo
from app.schemas.registration import RegistrationCreate
from app.services.audit_log import audit_log_service
from app.services.notification import notification_service

class RegistrationService:
    @staticmethod
    def register_for_event(
        db: Session,
        user_id: int,
        request: RegistrationCreate,
        background_tasks: BackgroundTasks
    ) -> Registration:
        event = event_repo.get(db, request.event_id)
        if not event:
            raise NotFoundException("Event not found")

        if event.status != "Published":
            raise BadRequestException(f"Cannot register for event because its status is '{event.status}'")

        if event.start_date <= datetime.now():
            raise BadRequestException("Cannot register for an event that has already started or completed")

        existing = registration_repo.get_by_event_and_user(db, event_id=request.event_id, user_id=user_id)
        if existing:
            if existing.status == "Confirmed":
                raise ConflictException("You are already registered for this event")
            else:
                active_count = registration_repo.get_active_count_by_event(db, request.event_id)
                if active_count >= event.capacity:
                    raise BadRequestException("Event is already at full capacity")

                updated = registration_repo.update(db, db_obj=existing, obj_in={"status": "Confirmed", "registration_date": datetime.now()})

                audit_log_service.log_action(db, action="Register Event", details={"event_id": event.id, "registration_id": updated.id}, user_id=user_id)

                user = user_repo.get(db, user_id)
                notification_service.trigger_registration_confirmation(background_tasks, email=user.email, full_name=user.full_name, event_name=event.name)
                return updated

        active_count = registration_repo.get_active_count_by_event(db, request.event_id)
        if active_count >= event.capacity:
            raise BadRequestException("Event is already at full capacity")

        reg_obj = {
            "event_id": request.event_id,
            "user_id": user_id,
            "status": "Confirmed"
        }
        registration = registration_repo.create(db, obj_in=reg_obj)

        audit_log_service.log_action(db, action="Register Event", details={"event_id": event.id, "registration_id": registration.id}, user_id=user_id)

        user = user_repo.get(db, user_id)
        notification_service.trigger_registration_confirmation(background_tasks, email=user.email, full_name=user.full_name, event_name=event.name)

        return registration

    @staticmethod
    def cancel_registration(db: Session, registration_id: int, user_id: int, is_admin: bool) -> Registration:
        registration = registration_repo.get(db, registration_id)
        if not registration:
            raise NotFoundException("Registration not found")

        if not is_admin and registration.user_id != user_id:
            raise ForbiddenException("You do not have permission to cancel this registration")

        if registration.status == "Cancelled":
            raise BadRequestException("Registration is already cancelled")

        updated = registration_repo.update(db, db_obj=registration, obj_in={"status": "Cancelled"})

        if registration.ticket:
            from app.repositories.ticket import ticket_repo
            ticket_repo.update(db, db_obj=registration.ticket, obj_in={"status": "Cancelled"})

        audit_log_service.log_action(db, action="Cancel Registration", details={"registration_id": registration_id}, user_id=user_id)

        return updated

    @staticmethod
    def get_user_history(db: Session, user_id: int, skip: int = 0, limit: int = 100):
        return registration_repo.get_user_history(db, user_id=user_id, skip=skip, limit=limit)

    @staticmethod
    def get_event_registrations(db: Session, event_id: int, user_id: int, is_admin: bool, skip: int = 0, limit: int = 100):
        event = event_repo.get(db, event_id)
        if not event:
            raise NotFoundException("Event not found")

        if not is_admin and event.organizer_id != user_id:
            raise ForbiddenException("You do not have permission to view registrations for this event")

        return registration_repo.get_event_registrations(db, event_id=event_id, skip=skip, limit=limit)

registration_service = RegistrationService()
