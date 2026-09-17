from sqlalchemy.orm import Session

from app.models.checkin import CheckIn


class CheckInRepository:

    @staticmethod
    def create(db: Session, checkin: CheckIn):
        db.add(checkin)
        db.commit()
        db.refresh(checkin)
        return checkin

    @staticmethod
    def get_by_id(db: Session, checkin_id: int):
        return (
            db.query(CheckIn)
            .filter(CheckIn.id == checkin_id)
            .first()
        )

    @staticmethod
    def get_by_registration(
        db: Session,
        registration_id: int
    ):
        return (
            db.query(CheckIn)
            .filter(
                CheckIn.registration_id == registration_id
            )
            .first()
        )

    @staticmethod
    def get_event_attendance(
        db: Session,
        event_id: int
    ):
        return (
            db.query(CheckIn)
            .join(
                CheckIn.registration
            )
            .filter(
                CheckIn.registration.has(
                    event_id=event_id
                )
            )
            .all()
        )

    @staticmethod
    def checkout(
        db: Session,
        checkin: CheckIn
    ):
        from datetime import datetime

        checkin.check_out_time = datetime.utcnow()

        db.commit()
        db.refresh(checkin)

        return checkin