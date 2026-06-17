from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.attendance import Attendance
from app.repositories.base import BaseRepository

class AttendanceRepository(BaseRepository[Attendance]):
    def __init__(self):
        super().__init__(Attendance)

    def get_by_event_and_user(self, db: Session, event_id: int, user_id: int) -> Optional[Attendance]:
        return db.query(Attendance).filter(
            Attendance.event_id == event_id,
            Attendance.user_id == user_id
        ).first()

    def get_event_attendance(self, db: Session, event_id: int) -> List[Attendance]:
        return db.query(Attendance).filter(Attendance.event_id == event_id).all()

    def get_user_attendance(self, db: Session, user_id: int) -> List[Attendance]:
        return db.query(Attendance).filter(Attendance.user_id == user_id).all()

attendance_repo = AttendanceRepository()
