from app.repositories.base import BaseRepository
from app.repositories.role import role_repo
from app.repositories.user import user_repo
from app.repositories.category import category_repo
from app.repositories.event import event_repo
from app.repositories.registration import registration_repo
from app.repositories.ticket import ticket_repo
from app.repositories.attendance import attendance_repo
from app.repositories.audit_log import audit_log_repo

__all__ = [
    "BaseRepository",
    "role_repo",
    "user_repo",
    "category_repo",
    "event_repo",
    "registration_repo",
    "ticket_repo",
    "attendance_repo",
    "audit_log_repo"
]
