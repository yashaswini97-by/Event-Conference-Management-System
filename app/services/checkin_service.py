from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.checkin import CheckIn

from app.repositories.checkin_repository import (
    CheckInRepository
)
from app.repositories.registration_repository import (
    RegistrationRepository
)
from app.repositories.event_repository import EventRepository

from app.utils.enums import RegistrationStatus


class CheckInService:

    @staticmethod
    def check_in(
        db: Session,
        registration_id: int,
        check_in_method
    ):

        registration = RegistrationRepository.get_by_id(
            db,
            registration_id
        )

        if not registration:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registration not found"
            )

        # Only confirmed attendees can check in
        if registration.registration_status != RegistrationStatus.CONFIRMED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only confirmed attendees can check in"
            )

        # Prevent duplicate check-in
        existing = CheckInRepository.get_by_registration(
            db,
            registration_id
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Attendee is already checked in"
            )

        checkin = CheckIn(
            registration_id=registration_id,
            check_in_time=datetime.utcnow(),
            check_in_method=check_in_method
        )

        # Change registration status to ATTENDED
        registration.registration_status = RegistrationStatus.ATTENDED

        db.add(registration)
        db.commit()

        return CheckInRepository.create(
            db,
            checkin
        )

    @staticmethod
    def check_out(
        db: Session,
        registration_id: int
    ):

        checkin = CheckInRepository.get_by_registration(
            db,
            registration_id
        )

        if not checkin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Check-in record not found"
            )

        if checkin.check_out_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Attendee is already checked out"
            )

        return CheckInRepository.checkout(
            db,
            checkin
        )

    @staticmethod
    def get_event_attendance(
        db: Session,
        event_id: int
    ):

        event = EventRepository.get_by_id(
            db,
            event_id
        )

        if not event or event.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )

        records = CheckInRepository.get_event_attendance(
            db,
            event_id
        )

        result = []

        for record in records:

            registration = record.registration

            result.append({
                "registration_id": registration.id,
                "attendee_id": registration.attendee_id,
                "attendee_name": registration.attendee.full_name,
                "check_in_time": record.check_in_time,
                "check_out_time": record.check_out_time,
                "check_in_method": record.check_in_method
            })

        return result