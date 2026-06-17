from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.schemas.role import RoleResponse

class UserBase(BaseModel):
    full_name: str = Field(..., examples=["John Doe"])
    email: EmailStr = Field(..., examples=["john@example.com"])
    phone: Optional[str] = Field(None, examples=["+1234567890"])
    is_active: bool = Field(True, examples=[True])

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, examples=["password123"])
    role_id: int = Field(..., examples=[3])

class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, examples=["John New Doe"])
    phone: Optional[str] = Field(None, examples=["+1987654321"])
    is_active: Optional[bool] = Field(None, examples=[True])

class UserResponse(UserBase):
    id: int
    role_id: int
    role: Optional[RoleResponse] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
