from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.attendee import Attendee


class AttendeeRepository:

    @staticmethod
    def create(
        db: Session,
        attendee: Attendee
    ):
        db.add(attendee)
        db.commit()
        db.refresh(attendee)

        return attendee

    @staticmethod
    def get_by_id(
        db: Session,
        attendee_id: int
    ):
        return db.scalar(
            select(Attendee).where(
                Attendee.id == attendee_id
            )
        )

    @staticmethod
    def get_by_email(
        db: Session,
        email: str
    ):
        return db.scalar(
            select(Attendee).where(
                Attendee.email == email
            )
        )

    @staticmethod
    def get_all(
        db: Session
    ):
        return db.scalars(
            select(Attendee)
            .order_by(Attendee.id.desc())
        ).all()

    @staticmethod
    def update(
        db: Session,
        attendee: Attendee,
        data: dict
    ):
        for key, value in data.items():
            setattr(attendee, key, value)

        db.commit()
        db.refresh(attendee)

        return attendee