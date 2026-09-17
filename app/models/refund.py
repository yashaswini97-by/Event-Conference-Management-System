from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey,
    Enum,
    Text,
)

from app.database import Base
from app.utils.enums import RefundStatus, RefundReason


class Refund(Base):
    __tablename__ = "refunds"

    id = Column(Integer, primary_key=True, index=True)

    payment_id = Column(
        Integer,
        ForeignKey("payments.id"),
        nullable=False,
        index=True,
    )

    purchase_id = Column(
        Integer,
        ForeignKey("purchases.id"),
        nullable=False,
        index=True,
    )

    amount = Column(
        Float,
        nullable=False,
    )

    reason = Column(
        Enum(RefundReason),
        nullable=False,
    )

    status = Column(
        Enum(RefundStatus),
        default=RefundStatus.REQUESTED,
        nullable=False,
    )

    remarks = Column(
        Text,
        nullable=True,
    )

    requested_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    processed_at = Column(
        DateTime,
        nullable=True,
    )

    processed_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
    )