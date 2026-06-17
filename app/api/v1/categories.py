from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services.category import category_service

router = APIRouter(prefix="/categories", tags=["Event Categories"])

@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    request: CategoryCreate,
    current_user: User = Depends(deps.RoleChecker(allowed_roles=["Admin"])),
    db: Session = Depends(get_db)
):
    return category_service.create_category(db, request)

@router.get("", response_model=List[CategoryResponse])
def list_categories(
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    return category_service.list_categories(db)

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    return category_service.get_category(db, category_id)

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    request: CategoryUpdate,
    current_user: User = Depends(deps.RoleChecker(allowed_roles=["Admin"])),
    db: Session = Depends(get_db)
):
    return category_service.update_category(db, category_id, request)

@router.delete("/{category_id}", response_model=CategoryResponse)
def delete_category(
    category_id: int,
    current_user: User = Depends(deps.RoleChecker(allowed_roles=["Admin"])),
    db: Session = Depends(get_db)
):
    return category_service.delete_category(db, category_id)
