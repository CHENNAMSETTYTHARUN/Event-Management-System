from fastapi import APIRouter, Depends, BackgroundTasks, status, Request
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, ChangePasswordRequest, Token
from app.schemas.user import UserResponse
from app.services.auth import auth_service
from app.core.exceptions import BadRequestException

router = APIRouter(prefix="/auth", tags=["Authentication"])

async def get_login_request(request: Request) -> LoginRequest:
    content_type = request.headers.get("content-type", "")
    if "application/x-www-form-urlencoded" in content_type:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        if not username or not password:
            raise BadRequestException("Missing username or password in form data")
        return LoginRequest(email=username, password=password)
    else:
        try:
            body = await request.json()
            return LoginRequest(**body)
        except Exception:
            raise BadRequestException("Invalid login request payload")

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    request: RegisterRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    return auth_service.register_user(db, request, background_tasks)

@router.post(
    "/login",
    response_model=Token,
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": LoginRequest.model_json_schema()
                },
                "application/x-www-form-urlencoded": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "username": {
                                "type": "string",
                                "description": "Email address",
                                "format": "email"
                            },
                            "password": {
                                "type": "string",
                                "format": "password"
                            }
                        },
                        "required": ["username", "password"]
                    }
                }
            }
        }
    }
)
async def login(
    request: LoginRequest = Depends(get_login_request),
    db: Session = Depends(get_db)
):
    return auth_service.authenticate_user(db, request)

@router.post("/refresh", response_model=Token)
def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    return auth_service.refresh_access_token(db, refresh_token)

@router.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    auth_service.change_password(db, current_user.id, request)
    return {"message": "Password changed successfully"}

@router.get("/profile", response_model=UserResponse)
def get_profile(
    current_user: User = Depends(deps.get_current_user)
):
    return current_user
