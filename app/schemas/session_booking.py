from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.utils.enums import SessionBookingStatus


class SessionBookingCreate(BaseModel):
    attendee_id: int


class SessionBookingResponse(BaseModel):
    id: int
    session_id: int
    attendee_id: int
    registration_id: int
    booking_date: datetime
    status: SessionBookingStatus

    model_config = ConfigDict(from_attributes=True)


class AttendeeSessionResponse(BaseModel):
    booking_id: int
    session_id: int
    event_id: int
    title: str
    description: str | None
    start_time: datetime
    end_time: datetime
    session_type: str
    status: SessionBookingStatus