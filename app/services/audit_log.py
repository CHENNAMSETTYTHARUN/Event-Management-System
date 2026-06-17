from sqlalchemy.orm import Session
from app.repositories.audit_log import audit_log_repo

class AuditLogService:
    @staticmethod
    def log_action(db: Session, action: str, details: dict, user_id: int = None):
        obj_in = {
            "user_id": user_id,
            "action": action,
            "details": details
        }
        return audit_log_repo.create(db, obj_in=obj_in)

    @staticmethod
    def get_logs_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
        return audit_log_repo.get_by_user(db, user_id=user_id, skip=skip, limit=limit)

audit_log_service = AuditLogService()
