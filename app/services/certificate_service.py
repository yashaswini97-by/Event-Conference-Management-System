import uuid
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.certificate import Certificate

from app.repositories.certificate_repository import (
    CertificateRepository
)

from app.repositories.registration_repository import (
    RegistrationRepository
)

from app.utils.enums import (
    RegistrationStatus,
    CertificateStatus
)


class CertificateService:

    @staticmethod
    def generate_certificate(
        db: Session,
        registration_id: int,
        certificate_type
    ):

        # Get registration
        registration = RegistrationRepository.get_by_id(
            db,
            registration_id
        )

        if not registration:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registration not found"
            )

        # Certificate only for attended participants
        if (
            registration.registration_status
            != RegistrationStatus.ATTENDED
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Certificate can be generated only for attended participants"
            )

        # Prevent duplicate certificate
        existing = CertificateRepository.get_by_registration(
            db,
            registration_id
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Certificate already generated"
            )

        # Generate certificate number
        certificate_number = (
            f"EVT-{datetime.utcnow().strftime('%Y%m%d')}-"
            f"{uuid.uuid4().hex[:8].upper()}"
        )

        certificate = Certificate(
            certificate_number=certificate_number,
            attendee_id=registration.attendee_id,
            event_id=registration.event_id,
            registration_id=registration.id,
            issue_date=datetime.utcnow(),
            certificate_type=certificate_type,
            status=CertificateStatus.GENERATED
        )

        return CertificateRepository.create(
            db,
            certificate
        )

    @staticmethod
    def get_certificate(
        db: Session,
        certificate_id: int
    ):

        certificate = CertificateRepository.get_by_id(
            db,
            certificate_id
        )

        if not certificate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Certificate not found"
            )

        return certificate

    @staticmethod
    def get_attendee_certificates(
        db: Session,
        attendee_id: int
    ):

        return CertificateRepository.get_by_attendee(
            db,
            attendee_id
        )