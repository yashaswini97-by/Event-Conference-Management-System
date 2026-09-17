from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.utils.enums import RegistrationStatus


class RegistrationCreate(BaseModel):
    attendee_id: int


class RegistrationResponse(BaseModel):
    id: int
    attendee_id: int
    event_id: int
    registration_date: datetime
    registration_status: RegistrationStatus

    model_config = ConfigDict(
        from_attributes=True
    )


class RegistrationCancelRequest(BaseModel):
    reason: str | None = None