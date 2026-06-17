from typing import List
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException, ConflictException
from app.models.category import EventCategory
from app.repositories.category import category_repo
from app.schemas.category import CategoryCreate, CategoryUpdate

class CategoryService:
    @staticmethod
    def create_category(db: Session, request: CategoryCreate) -> EventCategory:
        if category_repo.get_by_name(db, name=request.name):
            raise ConflictException("Category name already exists")
        return category_repo.create(db, obj_in=request.model_dump())

    @staticmethod
    def get_category(db: Session, category_id: int) -> EventCategory:
        cat = category_repo.get(db, category_id)
        if not cat:
            raise NotFoundException("Category not found")
        return cat

    @staticmethod
    def list_categories(db: Session, skip: int = 0, limit: int = 100) -> List[EventCategory]:
        return category_repo.get_multi(db, skip=skip, limit=limit)

    @staticmethod
    def update_category(db: Session, category_id: int, request: CategoryUpdate) -> EventCategory:
        cat = category_repo.get(db, category_id)
        if not cat:
            raise NotFoundException("Category not found")

        if request.name:
            existing = category_repo.get_by_name(db, name=request.name)
            if existing and existing.id != category_id:
                raise ConflictException("Category name already exists")

        return category_repo.update(db, db_obj=cat, obj_in=request.model_dump(exclude_unset=True))

    @staticmethod
    def delete_category(db: Session, category_id: int) -> EventCategory:
        cat = category_repo.get(db, category_id)
        if not cat:
            raise NotFoundException("Category not found")
        return category_repo.remove(db, id=category_id)

category_service = CategoryService()
