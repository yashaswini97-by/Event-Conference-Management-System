from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.utils.enums import AuditAction, AuditStatus


class AuditRepository:

    def create(
        self,
        db: Session,
        audit_log: AuditLog,
    ):

        db.add(audit_log)
        db.commit()
        db.refresh(audit_log)

        return audit_log

    def get_by_id(
        self,
        db: Session,
        audit_id: int,
    ):

        return db.query(
            AuditLog
        ).filter(
            AuditLog.id == audit_id
        ).first()

    def get_all(
        self,
        db: Session,
    ):

        return db.query(
            AuditLog
        ).order_by(
            AuditLog.created_at.desc()
        ).all()

    def get_by_user(
        self,
        db: Session,
        user_id: int,
    ):

        return db.query(
            AuditLog
        ).filter(
            AuditLog.user_id == user_id
        ).order_by(
            AuditLog.created_at.desc()
        ).all()

    def get_by_action(
        self,
        db: Session,
        action: AuditAction,
    ):

        return db.query(
            AuditLog
        ).filter(
            AuditLog.action == action
        ).order_by(
            AuditLog.created_at.desc()
        ).all()

    def get_failed_logins(
        self,
        db: Session,
        user_id: int,
    ):

        return db.query(
            AuditLog
        ).filter(
            AuditLog.user_id == user_id,
            AuditLog.action == AuditAction.LOGIN_FAILED,
            AuditLog.status == AuditStatus.FAILED,
        ).order_by(
            AuditLog.created_at.desc()
        ).all()