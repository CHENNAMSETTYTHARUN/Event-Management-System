from datetime import timedelta
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from app.core import security
from app.core.config import settings
from app.core.exceptions import ConflictException, UnauthorizedException, BadRequestException
from app.models.user import User
from app.repositories.user import user_repo
from app.repositories.role import role_repo
from app.schemas.auth import LoginRequest, RegisterRequest, Token, ChangePasswordRequest
from app.services.audit_log import audit_log_service
from app.services.notification import notification_service

class AuthService:
    @staticmethod
    def register_user(db: Session, request: RegisterRequest, background_tasks: BackgroundTasks) -> User:
        if user_repo.get_by_email(db, email=request.email):
            raise ConflictException("Email is already registered")

        if request.phone and user_repo.get_by_phone(db, phone=request.phone):
            raise ConflictException("Phone number is already registered")

        role = role_repo.get(db, request.role_id)
        if not role:
            raise BadRequestException("Invalid role ID")

        hashed_password = security.get_password_hash(request.password)
        user_data = request.model_dump()
        user_data["password"] = hashed_password

        new_user = user_repo.create(db, obj_in=user_data)

        audit_log_service.log_action(db, action="Register", details={"email": new_user.email}, user_id=new_user.id)

        notification_service.trigger_welcome_email(background_tasks, email=new_user.email, full_name=new_user.full_name)

        return new_user

    @staticmethod
    def authenticate_user(db: Session, request: LoginRequest) -> Token:
        user = user_repo.get_by_email(db, email=request.email)
        if not user or not security.verify_password(request.password, user.password):
            raise UnauthorizedException("Incorrect email or password")

        if not user.is_active:
            raise UnauthorizedException("User account is disabled")

        access_token = security.create_access_token(subject=user.id)
        refresh_token = security.create_refresh_token(subject=user.id)

        audit_log_service.log_action(db, action="Login", details={"email": user.email}, user_id=user.id)

        return Token(access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    def refresh_access_token(db: Session, refresh_token: str) -> Token:
        payload = security.decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise UnauthorizedException("Invalid refresh token")

        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedException("Invalid token payload")

        user = user_repo.get(db, int(user_id))
        if not user or not user.is_active:
            raise UnauthorizedException("User not active")

        new_access_token = security.create_access_token(subject=user.id)
        new_refresh_token = security.create_refresh_token(subject=user.id)

        return Token(access_token=new_access_token, refresh_token=new_refresh_token)

    @staticmethod
    def change_password(db: Session, user_id: int, request: ChangePasswordRequest):
        user = user_repo.get(db, user_id)
        if not user:
            raise UnauthorizedException("User not found")

        if not security.verify_password(request.old_password, user.password):
            raise BadRequestException("Incorrect old password")

        new_hashed = security.get_password_hash(request.new_password)
        user_repo.update(db, db_obj=user, obj_in={"password": new_hashed})

        audit_log_service.log_action(db, action="Change Password", details={}, user_id=user_id)

auth_service = AuthService()
