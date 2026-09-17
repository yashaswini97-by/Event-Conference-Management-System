from sqlalchemy.orm import Session

from app.models.certificate import Certificate


class CertificateRepository:

    @staticmethod
    def create(
        db: Session,
        certificate: Certificate
    ):
        db.add(certificate)
        db.commit()
        db.refresh(certificate)

        return certificate

    @staticmethod
    def get_by_id(
        db: Session,
        certificate_id: int
    ):
        return (
            db.query(Certificate)
            .filter(
                Certificate.id == certificate_id
            )
            .first()
        )

    @staticmethod
    def get_by_registration(
        db: Session,
        registration_id: int
    ):
        return (
            db.query(Certificate)
            .filter(
                Certificate.registration_id == registration_id
            )
            .first()
        )

    @staticmethod
    def get_by_attendee(
        db: Session,
        attendee_id: int
    ):
        return (
            db.query(Certificate)
            .filter(
                Certificate.attendee_id == attendee_id
            )
            .all()
        )