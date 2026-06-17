from sqlalchemy.orm import Session
from app.models.role import Role
from app.repositories.role import role_repo

class RoleService:
    @staticmethod
    def create_role(db: Session, name: str) -> Role:
        existing = role_repo.get_by_name(db, name)
        if existing:
            return existing
        return role_repo.create(db, obj_in={"name": name})

    @staticmethod
    def list_roles(db: Session):
        return role_repo.get_multi(db)

role_service = RoleService()
