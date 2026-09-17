from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.audit import AuditLogCreate, AuditLogResponse
from app.services.audit_service import AuditService
from app.utils.dependencies import require_roles
from app.utils.enums import UserRole


router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"]
)


@router.post(
    "",
    response_model=AuditLogResponse,
    status_code=status.HTTP_201_CREATED
)
def create_audit_log(
    data: AuditLogCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN
        )
    )
):
    return AuditService.create_audit_log(
        db,
        data
    )