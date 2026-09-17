from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.feedback import Feedback

from app.repositories.feedback_repository import (
    FeedbackRepository
)

from app.repositories.registration_repository import (
    RegistrationRepository
)

from app.repositories.event_repository import (
    EventRepository
)

from app.repositories.speaker_repository import (
    SpeakerRepository
)

from app.repositories.session_repository import (
    SessionRepository
)

from app.models.checkin import CheckIn

from app.utils.enums import RegistrationStatus


class FeedbackService:

    @staticmethod
    def create_feedback(
        db: Session,
        data
    ):

        # Check registration
        registration = RegistrationRepository.get_by_id(
            db,
            data.registration_id
        )

        if not registration:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registration not found"
            )

        # Registration must belong to event
        if registration.event_id != data.event_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration does not belong to this event"
            )

        # Only attended attendees can give feedback
        if (
            registration.registration_status
            != RegistrationStatus.ATTENDED
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only checked-in attendees can submit feedback"
            )

        # Verify check-in record
        checkin = (
            db.query(CheckIn)
            .filter(
                CheckIn.registration_id
                == data.registration_id
            )
            .first()
        )

        if not checkin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Attendee has not checked in"
            )

        # Check event
        event = EventRepository.get_by_id(
            db,
            data.event_id
        )

        if not event or event.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )

        # Validate speaker
        if data.speaker_id:

            speaker = SpeakerRepository.get_by_id(
                db,
                data.speaker_id
            )

            if not speaker or speaker.is_deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Speaker not found"
                )

            if not speaker.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Speaker is inactive"
                )

        # Validate session
        if data.session_id:

            session = SessionRepository.get_by_id(
                db,
                data.session_id
            )

            if not session or session.is_deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Session not found"
                )

            if session.event_id != data.event_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Session does not belong to this event"
                )

        # Prevent duplicate session feedback
        if data.session_id:

            existing = (
                FeedbackRepository
                .get_duplicate_session_feedback(
                    db,
                    data.registration_id,
                    data.session_id
                )
            )

            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Feedback already submitted for this session"
                )

        # Create feedback
        feedback = Feedback(
            registration_id=data.registration_id,
            event_id=data.event_id,
            speaker_id=data.speaker_id,
            session_id=data.session_id,
            rating=data.rating,
            feedback=data.feedback
        )

        return FeedbackRepository.create(
            db,
            feedback
        )

    @staticmethod
    def get_event_feedback(
        db: Session,
        event_id: int
    ):

        event = EventRepository.get_by_id(
            db,
            event_id
        )

        if not event or event.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )

        return FeedbackRepository.get_event_feedback(
            db,
            event_id
        )

    @staticmethod
    def get_speaker_rating(
        db: Session,
        speaker_id: int
    ):

        speaker = SpeakerRepository.get_by_id(
            db,
            speaker_id
        )

        if not speaker or speaker.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Speaker not found"
            )

        feedbacks = FeedbackRepository.get_speaker_feedback(
            db,
            speaker_id
        )

        total_reviews = len(feedbacks)

        if total_reviews == 0:
            average_rating = 0.0
        else:
            average_rating = round(
                sum(item.rating for item in feedbacks)
                / total_reviews,
                2
            )

        return {
            "speaker_id": speaker_id,
            "average_rating": average_rating,
            "total_reviews": total_reviews
        }