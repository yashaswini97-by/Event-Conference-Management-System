from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.utils.enums import CheckInMethod


class CheckInCreate(BaseModel):
    check_in_method: CheckInMethod


class CheckInResponse(BaseModel):
    id: int
    registration_id: int
    check_in_time: datetime
    check_out_time: datetime | None
    check_in_method: CheckInMethod

    model_config = ConfigDict(from_attributes=True)


class AttendanceResponse(BaseModel):
    registration_id: int
    attendee_id: int
    attendee_name: str
    check_in_time: datetime
    check_out_time: datetime | None
    check_in_method: CheckInMethod