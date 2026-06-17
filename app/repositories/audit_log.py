from typing import List
from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog
from app.repositories.base import BaseRepository

class AuditLogRepository(BaseRepository[AuditLog]):
    def __init__(self):
        super().__init__(AuditLog)

    def get_by_user(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        return db.query(AuditLog).filter(AuditLog.user_id == user_id).order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()

audit_log_repo = AuditLogRepository()
