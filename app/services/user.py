from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.user import user_repo

class UserService:
    @staticmethod
    def get_user(db: Session, user_id: int) -> User:
        return user_repo.get(db, user_id)

user_service = UserService()
