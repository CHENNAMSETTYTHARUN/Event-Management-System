from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.user import User
from app.schemas.role import RoleCreate, RoleResponse
from app.services.role import role_service

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(
    request: RoleCreate,
    current_user: User = Depends(deps.RoleChecker(allowed_roles=["Admin"])),
    db: Session = Depends(get_db)
):
    return role_service.create_role(db, request.name)

@router.get("", response_model=List[RoleResponse])
def list_roles(
    current_user: User = Depends(deps.RoleChecker(allowed_roles=["Admin"])),
    db: Session = Depends(get_db)
):
    return role_service.list_roles(db)
