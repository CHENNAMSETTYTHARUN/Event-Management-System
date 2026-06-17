from typing import Optional
from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from app.repositories.base import BaseRepository

class TicketRepository(BaseRepository[Ticket]):
    def __init__(self):
        super().__init__(Ticket)

    def get_by_ticket_number(self, db: Session, ticket_number: str) -> Optional[Ticket]:
        return db.query(Ticket).filter(Ticket.ticket_number == ticket_number).first()

    def get_by_registration_id(self, db: Session, registration_id: int) -> Optional[Ticket]:
        return db.query(Ticket).filter(Ticket.registration_id == registration_id).first()

ticket_repo = TicketRepository()
