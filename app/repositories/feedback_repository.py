from sqlalchemy.orm import Session

from app.models.feedback import Feedback


class FeedbackRepository:

    @staticmethod
    def create(
        db: Session,
        feedback: Feedback
    ):
        db.add(feedback)
        db.commit()
        db.refresh(feedback)

        return feedback

    @staticmethod
    def get_by_id(
        db: Session,
        feedback_id: int
    ):
        return (
            db.query(Feedback)
            .filter(
                Feedback.id == feedback_id
            )
            .first()
        )

    @staticmethod
    def get_duplicate_session_feedback(
        db: Session,
        registration_id: int,
        session_id: int
    ):
        return (
            db.query(Feedback)
            .filter(
                Feedback.registration_id == registration_id,
                Feedback.session_id == session_id
            )
            .first()
        )

    @staticmethod
    def get_event_feedback(
        db: Session,
        event_id: int
    ):
        return (
            db.query(Feedback)
            .filter(
                Feedback.event_id == event_id
            )
            .all()
        )

    @staticmethod
    def get_speaker_feedback(
        db: Session,
        speaker_id: int
    ):
        return (
            db.query(Feedback)
            .filter(
                Feedback.speaker_id == speaker_id
            )
            .all()
        )