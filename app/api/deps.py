from typing import List
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core import security
from app.core.database import get_db
from app.core.exceptions import UnauthorizedException, ForbiddenException
from app.models.user import User
from app.repositories.user import user_repo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    payload = security.decode_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Could not validate credentials")

    user = user_repo.get(db, int(user_id))
    if not user:
        raise UnauthorizedException("User not found")

    if not user.is_active:
        raise UnauthorizedException("Inactive user")

    return user

class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        role_name = current_user.role.name
        if role_name == "Admin":
            return current_user

        if role_name not in self.allowed_roles:
            raise ForbiddenException(f"Role '{role_name}' is not authorized to access this resource")

        return current_user
