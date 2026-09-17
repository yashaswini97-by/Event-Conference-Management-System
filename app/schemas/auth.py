from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.utils.enums import UserRole


class RegisterRequest(BaseModel):
    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    email: EmailStr

    phone: str | None = None

    password: str = Field(
        ...,
        min_length=6,
        max_length=100
    )

    role: UserRole = UserRole.ATTENDEE


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str | None
    role: UserRole
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str = Field(
        ...,
        min_length=6,
        max_length=100
    )