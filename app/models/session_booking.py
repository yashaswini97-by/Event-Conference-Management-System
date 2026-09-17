from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Enum,
    UniqueConstraint
)
from sqlalchemy.orm import relationship

from app.database import Base
from app.utils.enums import SessionBookingStatus


class SessionBooking(Base):
    __tablename__ = "session_bookings"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(
        Integer,
        ForeignKey("sessions.id"),
        nullable=False,
        index=True
    )

    attendee_id = Column(
        Integer,
        ForeignKey("attendees.id"),
        nullable=False,
        index=True
    )

    registration_id = Column(
        Integer,
        ForeignKey("registrations.id"),
        nullable=False,
        index=True
    )

    booking_date = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    status = Column(
        Enum(SessionBookingStatus),
        default=SessionBookingStatus.BOOKED,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    session = relationship("SessionModel")

    attendee = relationship("Attendee")

    registration = relationship("Registration")

    __table_args__ = (
        UniqueConstraint(
            "session_id",
            "attendee_id",
            name="uq_session_attendee_booking"
        ),
    )