from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SessionCreate(BaseModel):
    event_id: int
    speaker_id: int
    hall_id: int

    title: str = Field(
        ...,
        min_length=2,
        max_length=200
    )

    description: str | None = None

    start_time: datetime
    end_time: datetime

    capacity: int = Field(
        ...,
        gt=0
    )

    session_type: str = Field(
        ...,
        min_length=2,
        max_length=100
    )


class SessionUpdate(BaseModel):
    speaker_id: int | None = None
    hall_id: int | None = None

    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=200
    )

    description: str | None = None

    start_time: datetime | None = None
    end_time: datetime | None = None

    capacity: int | None = Field(
        default=None,
        gt=0
    )

    session_type: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )


class SessionResponse(BaseModel):
    id: int
    event_id: int
    speaker_id: int
    hall_id: int
    title: str
    description: str | None
    start_time: datetime
    end_time: datetime
    capacity: int
    session_type: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )