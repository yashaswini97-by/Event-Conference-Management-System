from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.feedback import (
    FeedbackCreate,
    FeedbackResponse,
    SpeakerRatingResponse
)

from app.services.feedback_service import (
    FeedbackService
)

from app.utils.dependencies import get_current_user


router = APIRouter(
    tags=["Feedback"]
)


@router.post(
    "/feedback",
    response_model=FeedbackResponse
)
def create_feedback(
    data: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return FeedbackService.create_feedback(
        db,
        data
    )


@router.get(
    "/events/{event_id}/feedback",
    response_model=list[FeedbackResponse]
)
def get_event_feedback(
    event_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return FeedbackService.get_event_feedback(
        db,
        event_id
    )


@router.get(
    "/speakers/{speaker_id}/ratings",
    response_model=SpeakerRatingResponse
)
def get_speaker_rating(
    speaker_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return FeedbackService.get_speaker_rating(
        db,
        speaker_id
    )