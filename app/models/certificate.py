from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint
)

from sqlalchemy.orm import relationship

from app.database import Base
from app.utils.enums import CertificateType, CertificateStatus


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)

    certificate_number = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    attendee_id = Column(
        Integer,
        ForeignKey("attendees.id"),
        nullable=False,
        index=True
    )

    event_id = Column(
        Integer,
        ForeignKey("events.id"),
        nullable=False,
        index=True
    )

    registration_id = Column(
        Integer,
        ForeignKey("registrations.id"),
        nullable=False,
        unique=True,
        index=True
    )

    issue_date = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    certificate_type = Column(
        Enum(CertificateType),
        nullable=False
    )

    status = Column(
        Enum(CertificateStatus),
        default=CertificateStatus.GENERATED,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    attendee = relationship("Attendee")
    event = relationship("Event")
    registration = relationship("Registration")

    __table_args__ = (
        UniqueConstraint(
            "attendee_id",
            "event_id",
            name="uq_certificate_attendee_event"
        ),
    )