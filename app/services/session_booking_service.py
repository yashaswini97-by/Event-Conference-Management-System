from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.session_booking import SessionBooking
from app.models.session import SessionModel
from app.models.registration import Registration


class SessionBookingService:

    @staticmethod
    def book_session(
        db: Session,
        session_id: int,
        attendee_id: int,
    ):
        # Check session
        session = (
            db.query(SessionModel)
            .filter(SessionModel.id == session_id)
            .first()
        )

        if not session:
            raise HTTPException(
                status_code=404,
                detail="Session not found"
            )

        # Check confirmed registration
        registration = (
            db.query(Registration)
            .filter(
                Registration.attendee_id == attendee_id,
                Registration.event_id == session.event_id,
                Registration.registration_status == "CONFIRMED",
            )
            .first()
        )

        if not registration:
            raise HTTPException(
                status_code=400,
                detail="Attendee must have a confirmed registration"
            )

        # Prevent duplicate booking
        existing = (
            db.query(SessionBooking)
            .filter(
                SessionBooking.session_id == session_id,
                SessionBooking.attendee_id == attendee_id,
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Session already booked"
            )

        # Check capacity
        booking_count = (
            db.query(SessionBooking)
            .filter(
                SessionBooking.session_id == session_id
            )
            .count()
        )

        if booking_count >= session.capacity:
            raise HTTPException(
                status_code=400,
                detail="Session capacity is full"
            )

        booking = SessionBooking(
            session_id=session_id,
            attendee_id=attendee_id,
            status="CONFIRMED",
        )

        db.add(booking)
        db.commit()
        db.refresh(booking)

        return booking

    @staticmethod
    def get_attendee_sessions(
        db: Session,
        attendee_id: int,
    ):
        return (
            db.query(SessionBooking)
            .filter(
                SessionBooking.attendee_id == attendee_id
            )
            .all()
        )

    @staticmethod
    def cancel_booking(
        db: Session,
        session_id: int,
        attendee_id: int,
    ):
        booking = (
            db.query(SessionBooking)
            .filter(
                SessionBooking.session_id == session_id,
                SessionBooking.attendee_id == attendee_id,
            )
            .first()
        )

        if not booking:
            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        db.delete(booking)
        db.commit()

        return {
            "message": "Session booking cancelled successfully"
        }