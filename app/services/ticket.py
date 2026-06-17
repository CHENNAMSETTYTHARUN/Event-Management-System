import uuid
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException, ConflictException, BadRequestException, ForbiddenException
from app.models.ticket import Ticket
from app.repositories.ticket import ticket_repo
from app.repositories.registration import registration_repo
from app.repositories.user import user_repo
from app.utils.qr import generate_qr_code
from app.services.audit_log import audit_log_service
from app.services.notification import notification_service

class TicketService:
    @staticmethod
    def generate_ticket(
        db: Session,
        registration_id: int,
        user_id: int,
        is_admin: bool,
        background_tasks: BackgroundTasks
    ) -> Ticket:
        registration = registration_repo.get(db, registration_id)
        if not registration:
            raise NotFoundException("Registration not found")

        event = registration.event
        if not is_admin and registration.user_id != user_id and event.organizer_id != user_id:
            raise ForbiddenException("You do not have permission to generate a ticket for this registration")

        if registration.status != "Confirmed":
            raise BadRequestException("Cannot generate a ticket for a cancelled registration")

        existing = ticket_repo.get_by_registration_id(db, registration_id)
        if existing:
            raise ConflictException("Ticket has already been generated for this registration")

        ticket_number = f"TKT-{registration_id}-{uuid.uuid4().hex[:8].upper()}"

        qr_payload = f"TICKET_NUMBER:{ticket_number};EVENT_ID:{event.id}"
        qr_code_base64 = generate_qr_code(qr_payload)

        ticket_obj = {
            "registration_id": registration_id,
            "ticket_number": ticket_number,
            "qr_code": qr_code_base64,
            "status": "Active"
        }

        ticket = ticket_repo.create(db, obj_in=ticket_obj)

        audit_log_service.log_action(db, action="Generate Ticket", details={"ticket_id": ticket.id, "ticket_number": ticket_number}, user_id=user_id)

        participant = user_repo.get(db, registration.user_id)
        notification_service.trigger_ticket_email(
            background_tasks,
            email=participant.email,
            full_name=participant.full_name,
            event_name=event.name,
            ticket_number=ticket_number
        )

        return ticket

    @staticmethod
    def get_ticket(db: Session, ticket_id: int, user_id: int, is_admin: bool) -> Ticket:
        ticket = ticket_repo.get(db, ticket_id)
        if not ticket:
            raise NotFoundException("Ticket not found")

        registration = ticket.registration
        event = registration.event
        if not is_admin and registration.user_id != user_id and event.organizer_id != user_id:
            raise ForbiddenException("You do not have permission to view this ticket")

        return ticket

    @staticmethod
    def get_ticket_by_number(db: Session, ticket_number: str, user_id: int, is_admin: bool) -> Ticket:
        ticket = ticket_repo.get_by_ticket_number(db, ticket_number)
        if not ticket:
            raise NotFoundException("Ticket not found")

        registration = ticket.registration
        event = registration.event
        if not is_admin and registration.user_id != user_id and event.organizer_id != user_id:
            raise ForbiddenException("You do not have permission to view this ticket")

        return ticket

    @staticmethod
    def validate_ticket(db: Session, ticket_number: str, event_id: int, user_id: int, is_admin: bool) -> dict:
        ticket = ticket_repo.get_by_ticket_number(db, ticket_number)
        if not ticket:
            return {"valid": False, "message": "Ticket not found", "ticket": None}

        registration = ticket.registration
        event = registration.event

        if not is_admin and event.organizer_id != user_id:
            raise ForbiddenException("Only the event organizer or Admin can validate tickets")

        if registration.event_id != event_id:
            return {"valid": False, "message": "Ticket is registered for a different event", "ticket": ticket}

        if registration.status == "Cancelled":
            return {"valid": False, "message": "Registration for this ticket is cancelled", "ticket": ticket}

        if ticket.status == "Cancelled":
            return {"valid": False, "message": "Ticket has been cancelled", "ticket": ticket}

        if ticket.status == "Used":
            return {"valid": False, "message": "Ticket has already been used", "ticket": ticket}

        return {"valid": True, "message": "Ticket is valid", "ticket": ticket}

    @staticmethod
    def cancel_ticket(db: Session, ticket_id: int, user_id: int, is_admin: bool) -> Ticket:
        ticket = ticket_repo.get(db, ticket_id)
        if not ticket:
            raise NotFoundException("Ticket not found")

        registration = ticket.registration
        event = registration.event
        if not is_admin and registration.user_id != user_id and event.organizer_id != user_id:
            raise ForbiddenException("You do not have permission to cancel this ticket")

        if ticket.status == "Cancelled":
            raise BadRequestException("Ticket is already cancelled")

        updated = ticket_repo.update(db, db_obj=ticket, obj_in={"status": "Cancelled"})

        audit_log_service.log_action(db, action="Cancel Ticket", details={"ticket_id": ticket_id}, user_id=user_id)

        return updated

ticket_service = TicketService()
