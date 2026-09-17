from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SpeakerCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    phone: str | None = None
    bio: str | None = None
    expertise: str | None = None
    company: str | None = None
    experience: int = Field(default=0, ge=0)


class SpeakerUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    email: EmailStr | None = None
    phone: str | None = None
    bio: str | None = None
    expertise: str | None = None
    company: str | None = None
    experience: int | None = Field(default=None, ge=0)


class SpeakerResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str | None
    bio: str | None
    expertise: str | None
    company: str | None
    experience: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SpeakerStatusResponse(BaseModel):
    message: str
    speaker_id: int
    is_active: bool