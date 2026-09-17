from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Enum
from sqlalchemy.orm import relationship

from app.database import Base
from app.utils.enums import CheckInMethod


class CheckIn(Base):
    __tablename__ = "check_ins"

    id = Column(Integer, primary_key=True, index=True)

    registration_id = Column(
        Integer,
        ForeignKey("registrations.id"),
        nullable=False,
        unique=True,
        index=True
    )

    check_in_time = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    check_out_time = Column(
        DateTime,
        nullable=True
    )

    check_in_method = Column(
        Enum(CheckInMethod),
        nullable=False
    )

    registration = relationship("Registration")

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )