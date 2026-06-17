from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.registration import Registration
from app.repositories.base import BaseRepository

class RegistrationRepository(BaseRepository[Registration]):
    def __init__(self):
        super().__init__(Registration)

    def get_by_event_and_user(self, db: Session, event_id: int, user_id: int) -> Optional[Registration]:
        return db.query(Registration).filter(
            Registration.event_id == event_id,
            Registration.user_id == user_id
        ).first()

    def get_active_count_by_event(self, db: Session, event_id: int) -> int:
        return db.query(Registration).filter(
            Registration.event_id == event_id,
            Registration.status == "Confirmed"
        ).count()

    def get_user_history(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Registration]:
        return db.query(Registration).filter(
            Registration.user_id == user_id
        ).order_by(Registration.registration_date.desc()).offset(skip).limit(limit).all()

    def get_event_registrations(self, db: Session, event_id: int, skip: int = 0, limit: int = 100) -> List[Registration]:
        return db.query(Registration).filter(
            Registration.event_id == event_id
        ).order_by(Registration.registration_date.desc()).offset(skip).limit(limit).all()

registration_repo = RegistrationRepository()
