from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class AttendeeCreate(BaseModel):
    full_name: str = Field(
        ...,
        min_length=2,
        max_length=150
    )

    email: EmailStr

    phone: str | None = None

    organization: str | None = None

    designation: str | None = None


class AttendeeUpdate(BaseModel):
    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150
    )

    email: EmailStr | None = None

    phone: str | None = None

    organization: str | None = None

    designation: str | None = None


class AttendeeResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str | None
    organization: str | None
    designation: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )