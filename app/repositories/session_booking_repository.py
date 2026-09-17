from sqlalchemy.orm import Session

from app.models.session_booking import SessionBooking
from app.utils.enums import SessionBookingStatus


class SessionBookingRepository:

    @staticmethod
    def create(db: Session, booking: SessionBooking):
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return booking

    @staticmethod
    def get_by_id(db: Session, booking_id: int):
        return (
            db.query(SessionBooking)
            .filter(SessionBooking.id == booking_id)
            .first()
        )

    @staticmethod
    def get_by_session_and_attendee(
        db: Session,
        session_id: int,
        attendee_id: int
    ):
        return (
            db.query(SessionBooking)
            .filter(
                SessionBooking.session_id == session_id,
                SessionBooking.attendee_id == attendee_id,
                SessionBooking.status == SessionBookingStatus.BOOKED
            )
            .first()
        )

    @staticmethod
    def count_bookings(
        db: Session,
        session_id: int
    ):
        return (
            db.query(SessionBooking)
            .filter(
                SessionBooking.session_id == session_id,
                SessionBooking.status == SessionBookingStatus.BOOKED
            )
            .count()
        )

    @staticmethod
    def get_attendee_sessions(
        db: Session,
        attendee_id: int
    ):
        return (
            db.query(SessionBooking)
            .filter(
                SessionBooking.attendee_id == attendee_id,
                SessionBooking.status == SessionBookingStatus.BOOKED
            )
            .all()
        )

    @staticmethod
    def cancel(
        db: Session,
        booking: SessionBooking
    ):
        booking.status = SessionBookingStatus.CANCELLED

        db.commit()
        db.refresh(booking)

        return booking