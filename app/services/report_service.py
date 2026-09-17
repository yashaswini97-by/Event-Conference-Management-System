from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.schemas.report import ReportCreate


class ReportService:

    @staticmethod
    def create_report(db: Session, data: ReportCreate):
        report = AuditLog(
            action=data.report_type,
            entity_type="REPORT",
            description=data.title,
            status="SUCCESS"
        )

        db.add(report)
        db.commit()
        db.refresh(report)

        return report

    @staticmethod
    def get_report(db: Session, report_id: int):
        report = db.query(AuditLog).filter(
            AuditLog.id == report_id
        ).first()

        if not report:
            raise HTTPException(
                status_code=404,
                detail="Report not found"
            )

        return report