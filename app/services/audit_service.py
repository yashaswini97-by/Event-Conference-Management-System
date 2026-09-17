from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.repositories.audit_repository import AuditRepository

from app.utils.enums import (
    AuditAction,
    AuditStatus,
)


class AuditService:

    def __init__(self):
        self.repo = AuditRepository()

    def create_log(
        self,
        db: Session,
        user_id: int | None,
        action: AuditAction,
        status: AuditStatus,
        description: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ):

        audit = AuditLog(
            user_id=user_id,
            action=action,
            status=status,
            description=description,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        return self.repo.create(
            db,
            audit,
        )

    def get_all(
        self,
        db: Session,
    ):

        return self.repo.get_all(db)

    def get_by_user(
        self,
        db: Session,
        user_id: int,
    ):

        return self.repo.get_by_user(
            db,
            user_id,
        )