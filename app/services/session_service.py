from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.event import Event
from app.models.hall import Hall
from app.models.session import SessionModel
from app.models.speaker import Speaker

from app.repositories.session_repository import SessionRepository
from app.schemas.session import SessionCreate, SessionUpdate


class SessionService:

    @staticmethod
    def validate_event(
        db: Session,
        event_id: int
    ):
        event = db.get(Event, event_id)

        if not event or event.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )

        return event

    @staticmethod
    def validate_speaker(
        db: Session,
        speaker_id: int
    ):
        speaker = db.get(
            Speaker,
            speaker_id
        )

        if not speaker or speaker.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Speaker not found"
            )

        if not speaker.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive speaker cannot be assigned"
            )

        return speaker

    @staticmethod
    def validate_hall(
        db: Session,
        hall_id: int
    ):
        hall = db.get(
            Hall,
            hall_id
        )

        if not hall or hall.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Hall not found"
            )

        return hall

    @staticmethod
    def validate_times(
        event,
        start_time,
        end_time
    ):
        if end_time <= start_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session end time must be after start time"
            )

        if start_time < event.start_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session cannot start before event starts"
            )

        if end_time > event.end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session cannot end after event ends"
            )

    @staticmethod
    def validate_capacity(
        hall,
        capacity
    ):
        if capacity > hall.capacity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session capacity cannot exceed hall capacity"
            )

    @staticmethod
    def validate_overlaps(
        db,
        hall_id,
        speaker_id,
        start_time,
        end_time,
        exclude_id=None
    ):
        hall_overlap = SessionRepository.get_hall_overlap(
            db,
            hall_id,
            start_time,
            end_time,
            exclude_id
        )

        if hall_overlap:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Hall is already booked for another session during this time"
            )

        speaker_overlap = SessionRepository.get_speaker_overlap(
            db,
            speaker_id,
            start_time,
            end_time,
            exclude_id
        )

        if speaker_overlap:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Speaker already has another session during this time"
            )

    @staticmethod
    def create_session(
        db: Session,
        data: SessionCreate
    ):
        event = SessionService.validate_event(
            db,
            data.event_id
        )

        speaker = SessionService.validate_speaker(
            db,
            data.speaker_id
        )

        hall = SessionService.validate_hall(
            db,
            data.hall_id
        )

        SessionService.validate_times(
            event,
            data.start_time,
            data.end_time
        )

        SessionService.validate_capacity(
            hall,
            data.capacity
        )

        SessionService.validate_overlaps(
            db,
            data.hall_id,
            data.speaker_id,
            data.start_time,
            data.end_time
        )

        session = SessionModel(
            event_id=data.event_id,
            speaker_id=data.speaker_id,
            hall_id=data.hall_id,
            title=data.title,
            description=data.description,
            start_time=data.start_time,
            end_time=data.end_time,
            capacity=data.capacity,
            session_type=data.session_type
        )

        return SessionRepository.create(
            db,
            session
        )

    @staticmethod
    def get_session(
        db: Session,
        session_id: int
    ):
        session = SessionRepository.get_by_id(
            db,
            session_id
        )

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )

        return session

    @staticmethod
    def get_event_sessions(
        db: Session,
        event_id: int
    ):
        SessionService.validate_event(
            db,
            event_id
        )

        return SessionRepository.get_by_event(
            db,
            event_id
        )

    @staticmethod
    def update_session(
        db: Session,
        session_id: int,
        data: SessionUpdate
    ):
        session = SessionService.get_session(
            db,
            session_id
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        event = SessionService.validate_event(
            db,
            session.event_id
        )

        speaker_id = update_data.get(
            "speaker_id",
            session.speaker_id
        )

        hall_id = update_data.get(
            "hall_id",
            session.hall_id
        )

        start_time = update_data.get(
            "start_time",
            session.start_time
        )

        end_time = update_data.get(
            "end_time",
            session.end_time
        )

        capacity = update_data.get(
            "capacity",
            session.capacity
        )

        SessionService.validate_speaker(
            db,
            speaker_id
        )

        hall = SessionService.validate_hall(
            db,
            hall_id
        )

        SessionService.validate_times(
            event,
            start_time,
            end_time
        )

        SessionService.validate_capacity(
            hall,
            capacity
        )

        SessionService.validate_overlaps(
            db,
            hall_id,
            speaker_id,
            start_time,
            end_time,
            session_id
        )

        return SessionRepository.update(
            db,
            session,
            update_data
        )

    @staticmethod
    def delete_session(
        db: Session,
        session_id: int
    ):
        session = SessionService.get_session(
            db,
            session_id
        )

        SessionRepository.delete(
            db,
            session
        )