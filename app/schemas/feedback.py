from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class FeedbackCreate(BaseModel):

    registration_id: int

    event_id: int

    speaker_id: int | None = None

    session_id: int | None = None

    rating: int = Field(
        ...,
        ge=1,
        le=5
    )

    feedback: str | None = None


class FeedbackResponse(BaseModel):

    id: int
    registration_id: int
    event_id: int
    speaker_id: int | None
    session_id: int | None
    rating: int
    feedback: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SpeakerRatingResponse(BaseModel):

    speaker_id: int
    average_rating: float
    total_reviews: int