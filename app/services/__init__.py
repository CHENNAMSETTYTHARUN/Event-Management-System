from app.services.audit_log import audit_log_service
from app.services.auth import auth_service
from app.services.user import user_service
from app.services.role import role_service
from app.services.category import category_service
from app.services.event import event_service
from app.services.registration import registration_service
from app.services.ticket import ticket_service
from app.services.attendance import attendance_service
from app.services.dashboard import dashboard_service
from app.services.report import report_service
from app.services.notification import notification_service

__all__ = [
    "audit_log_service",
    "auth_service",
    "user_service",
    "role_service",
    "category_service",
    "event_service",
    "registration_service",
    "ticket_service",
    "attendance_service",
    "dashboard_service",
    "report_service",
    "notification_service"
]
