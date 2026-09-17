from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.certificate import (
    CertificateCreate,
    CertificateResponse
)

from app.services.certificate_service import (
    CertificateService
)

from app.utils.dependencies import get_current_user


router = APIRouter(
    tags=["Certificates"]
)


@router.post(
    "/certificates/generate/{registration_id}",
    response_model=CertificateResponse
)
def generate_certificate(
    registration_id: int,
    data: CertificateCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return CertificateService.generate_certificate(
        db,
        registration_id,
        data.certificate_type
    )


@router.get(
    "/certificates/{certificate_id}",
    response_model=CertificateResponse
)
def get_certificate(
    certificate_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return CertificateService.get_certificate(
        db,
        certificate_id
    )


@router.get(
    "/attendees/{attendee_id}/certificates",
    response_model=list[CertificateResponse]
)
def get_attendee_certificates(
    attendee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return CertificateService.get_attendee_certificates(
        db,
        attendee_id
    )