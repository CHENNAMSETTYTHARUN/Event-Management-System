from typing import Optional
from sqlalchemy.orm import Session
from app.models.role import Role
from app.repositories.base import BaseRepository

class RoleRepository(BaseRepository[Role]):
    def __init__(self):
        super().__init__(Role)

    def get_by_name(self, db: Session, name: str) -> Optional[Role]:
        return db.query(Role).filter(Role.name == name).first()

role_repo = RoleRepository()
