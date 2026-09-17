from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.registration import Registration
from app.utils.enums import RegistrationStatus


class RegistrationRepository:

    @staticmethod
    def create(
        db: Session,
        registration: Registration
    ):
        db.add(registration)
        db.commit()
        db.refresh(registration)

        return registration

    @staticmethod
    def get_by_id(
        db: Session,
        registration_id: int
    ):
        return db.scalar(
            select(Registration).where(
                Registration.id == registration_id
            )
        )

    @staticmethod
    def get_duplicate(
        db: Session,
        attendee_id: int,
        event_id: int
    ):
        return db.scalar(
            select(Registration).where(
                Registration.attendee_id == attendee_id,
                Registration.event_id == event_id,
                Registration.registration_status !=
                RegistrationStatus.CANCELLED
            )
        )

    @staticmethod
    def count_active_registrations(
        db: Session,
        event_id: int
    ):
        return db.scalar(
            select(func.count(Registration.id))
            .where(
                Registration.event_id == event_id,
                Registration.registration_status !=
                RegistrationStatus.CANCELLED
            )
        ) or 0

    @staticmethod
    def get_all(
        db: Session,
        event_id: int | None = None,
        registration_status: RegistrationStatus | None = None
    ):
        query = select(Registration)

        if event_id is not None:
            query = query.where(
                Registration.event_id == event_id
            )

        if registration_status is not None:
            query = query.where(
                Registration.registration_status ==
                registration_status
            )

        query = query.order_by(
            Registration.registration_date.desc()
        )

        return db.scalars(query).all()

    @staticmethod
    def update(
        db: Session,
        registration: Registration,
        data: dict
    ):
        for key, value in data.items():
            setattr(registration, key, value)

        db.commit()
        db.refresh(registration)

        return registration