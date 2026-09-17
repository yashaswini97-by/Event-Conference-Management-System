from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Enum,
)

from app.database import Base
from app.utils.enums import AuditAction, AuditStatus


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    action = Column(
        Enum(AuditAction),
        nullable=False,
        index=True,
    )

    status = Column(
        Enum(AuditStatus),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    ip_address = Column(
        String(100),
        nullable=True,
    )

    user_agent = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True,
    )