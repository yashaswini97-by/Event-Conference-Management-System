from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.session import SessionModel


class SessionRepository:

    @staticmethod
    def create(
        db: Session,
        session: SessionModel
    ):
        db.add(session)
        db.commit()
        db.refresh(session)

        return session

    @staticmethod
    def get_by_id(
        db: Session,
        session_id: int
    ):
        return db.scalar(
            select(SessionModel).where(
                SessionModel.id == session_id,
                SessionModel.is_deleted == False
            )
        )

    @staticmethod
    def get_by_event(
        db: Session,
        event_id: int
    ):
        return db.scalars(
            select(SessionModel)
            .where(
                SessionModel.event_id == event_id,
                SessionModel.is_deleted == False
            )
            .order_by(SessionModel.start_time)
        ).all()

    @staticmethod
    def get_hall_overlap(
        db: Session,
        hall_id: int,
        start_time,
        end_time,
        exclude_id: int | None = None
    ):
        query = select(SessionModel).where(
            SessionModel.hall_id == hall_id,
            SessionModel.is_deleted == False,
            SessionModel.start_time < end_time,
            SessionModel.end_time > start_time
        )

        if exclude_id is not None:
            query = query.where(
                SessionModel.id != exclude_id
            )

        return db.scalar(query)

    @staticmethod
    def get_speaker_overlap(
        db: Session,
        speaker_id: int,
        start_time,
        end_time,
        exclude_id: int | None = None
    ):
        query = select(SessionModel).where(
            SessionModel.speaker_id == speaker_id,
            SessionModel.is_deleted == False,
            SessionModel.start_time < end_time,
            SessionModel.end_time > start_time
        )

        if exclude_id is not None:
            query = query.where(
                SessionModel.id != exclude_id
            )

        return db.scalar(query)

    @staticmethod
    def update(
        db: Session,
        session: SessionModel,
        data: dict
    ):
        for key, value in data.items():
            setattr(session, key, value)

        db.commit()
        db.refresh(session)

        return session

    @staticmethod
    def delete(
        db: Session,
        session: SessionModel
    ):
        session.is_deleted = True

        db.commit()