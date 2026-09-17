from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)

    registration_id = Column(
        Integer,
        ForeignKey("registrations.id"),
        nullable=False
    )

    event_id = Column(
        Integer,
        ForeignKey("events.id"),
        nullable=False
    )

    speaker_id = Column(
        Integer,
        ForeignKey("speakers.id"),
        nullable=True
    )

    session_id = Column(
        Integer,
        ForeignKey("sessions.id"),
        nullable=True
    )

    rating = Column(Integer, nullable=False)

    feedback = Column(Text, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    registration = relationship("Registration")
    event = relationship("Event")
    speaker = relationship("Speaker")
    session = relationship("SessionModel")