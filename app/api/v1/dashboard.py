from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.user import User
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("", response_model=DashboardResponse)
def get_dashboard(
    current_user: User = Depends(deps.RoleChecker(allowed_roles=["Organizer"])),
    db: Session = Depends(get_db)
):
    is_admin = current_user.role.name == "Admin"
    return dashboard_service.get_dashboard_metrics(db, user_id=current_user.id, is_admin=is_admin)
