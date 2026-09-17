from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.utils.enums import CertificateType, CertificateStatus


class CertificateCreate(BaseModel):
    certificate_type: CertificateType = CertificateType.PARTICIPATION


class CertificateResponse(BaseModel):
    id: int
    certificate_number: str
    attendee_id: int
    event_id: int
    registration_id: int
    issue_date: datetime
    certificate_type: CertificateType
    status: CertificateStatus

    model_config = ConfigDict(from_attributes=True)