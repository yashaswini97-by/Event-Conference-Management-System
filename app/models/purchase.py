from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.utils.enums import PurchaseStatus


class Purchase(Base):
    __tablename__ = "purchases"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    registration_id: Mapped[int] = mapped_column(
        ForeignKey("registrations.id"),
        nullable=False,
        index=True
    )

    ticket_id: Mapped[int] = mapped_column(
        ForeignKey("tickets.id"),
        nullable=False,
        index=True
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    subtotal: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    discount: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False
    )

    tax: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False
    )

    total_amount: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    status: Mapped[PurchaseStatus] = mapped_column(
        Enum(PurchaseStatus),
        default=PurchaseStatus.PENDING,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )