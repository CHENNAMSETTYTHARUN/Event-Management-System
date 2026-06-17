from pydantic import BaseModel, EmailStr, Field

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str
    exp: int
    type: str

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., examples=["admin@example.com"])
    password: str = Field(..., min_length=6, examples=["admin123"])

class RegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=2, examples=["John Doe"])
    email: EmailStr = Field(..., examples=["john@example.com"])
    phone: str = Field(None, examples=["+1234567890"])
    password: str = Field(..., min_length=6, examples=["password123"])
    role_id: int = Field(..., description="1 = Admin, 2 = Organizer, 3 = Participant", examples=[3])

class ChangePasswordRequest(BaseModel):
    old_password: str = Field(..., examples=["password123"])
    new_password: str = Field(..., min_length=6, examples=["newpassword123"])
