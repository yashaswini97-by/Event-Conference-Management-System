from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.session_booking import (
    SessionBookingCreate,
    SessionBookingResponse,
    AttendeeSessionResponse
)
from app.services.session_booking_service import SessionBookingService
from app.utils.dependencies import get_current_user


router = APIRouter(
    tags=["Session Bookings"]
)


@router.post(
    "/sessions/{session_id}/book",
    response_model=SessionBookingResponse
)
def book_session(
    session_id: int,
    data: SessionBookingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return SessionBookingService.book_session(
        db,
        session_id,
        data.attendee_id
    )


@router.get(
    "/attendees/{attendee_id}/sessions",
    response_model=list[AttendeeSessionResponse]
)
def get_attendee_sessions(
    attendee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    bookings = SessionBookingService.get_attendee_sessions(
        db,
        attendee_id
    )

    result = []

    for booking in bookings:

        session = booking.session

        result.append(
            AttendeeSessionResponse(
                booking_id=booking.id,
                session_id=session.id,
                event_id=session.event_id,
                title=session.title,
                description=session.description,
                start_time=session.start_time,
                end_time=session.end_time,
                session_type=session.session_type,
                status=booking.status
            )
        )

    return result


@router.delete(
    "/session-bookings/{booking_id}",
    response_model=SessionBookingResponse
)
def cancel_session_booking(
    booking_id: int,
    attendee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return SessionBookingService.cancel_booking(
        db,
        booking_id,
        attendee_id
    )