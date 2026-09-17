from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.utils.enums import EventStatus, EventType


class EventCreate(BaseModel):
    event_name: str = Field(..., min_length=2, max_length=200)

    description: str | None = None

    event_type: EventType

    city: str = Field(..., min_length=2, max_length=100)

    start_date: datetime

    end_date: datetime

    registration_start: datetime

    registration_end: datetime

    capacity: int = Field(..., gt=0)

    status: EventStatus = EventStatus.DRAFT


class EventUpdate(BaseModel):
    event_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=200
    )

    description: str | None = None

    event_type: EventType | None = None

    city: str | None = None

    start_date: datetime | None = None

    end_date: datetime | None = None

    registration_start: datetime | None = None

    registration_end: datetime | None = None

    capacity: int | None = Field(
        default=None,
        gt=0
    )

    status: EventStatus | None = None


class EventResponse(BaseModel):
    id: int
    event_name: str
    description: str | None
    event_type: EventType
    organizer_id: int
    city: str
    start_date: datetime
    end_date: datetime
    registration_start: datetime
    registration_end: datetime
    capacity: int
    status: EventStatus

    model_config = ConfigDict(
        from_attributes=True
    )