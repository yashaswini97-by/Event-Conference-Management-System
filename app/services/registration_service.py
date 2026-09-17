from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.event import Event
from app.models.registration import Registration
from app.repositories.attendee_repository import AttendeeRepository
from app.repositories.registration_repository import RegistrationRepository
from app.schemas.registration import RegistrationCreate
from app.utils.enums import EventStatus, RegistrationStatus


class RegistrationService:

    @staticmethod
    def register_attendee(
        db: Session,
        event_id: int,
        data: RegistrationCreate
    ):

        # 1. Check event
        event = db.get(
            Event,
            event_id
        )

        if not event or event.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )

        # 2. Cancelled event check
        if event.status == EventStatus.CANCELLED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cancelled event cannot accept registrations"
            )

        # 3. Check attendee
        attendee = AttendeeRepository.get_by_id(
            db,
            data.attendee_id
        )

        if not attendee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attendee not found"
            )

        if not attendee.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive attendee cannot register"
            )

        now = datetime.utcnow()

        # 4. Registration period
        if now < event.registration_start:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Event registration has not started"
            )

        if now > event.registration_end:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Event registration has closed"
            )

        # 5. Duplicate registration
        duplicate = RegistrationRepository.get_duplicate(
            db,
            data.attendee_id,
            event_id
        )

        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Attendee is already registered for this event"
            )

        # 6. Capacity
        current_count = (
            RegistrationRepository.count_active_registrations(
                db,
                event_id
            )
        )

        if current_count >= event.capacity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Event registration capacity is full"
            )

        # 7. Create registration
        registration = Registration(
            attendee_id=data.attendee_id,
            event_id=event_id,
            registration_status=RegistrationStatus.PENDING
        )

        return RegistrationRepository.create(
            db,
            registration
        )

    @staticmethod
    def get_registration(
        db: Session,
        registration_id: int
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

        return registration

    @staticmethod
    def get_registrations(
        db: Session,
        event_id=None,
        registration_status=None
    ):
        return RegistrationRepository.get_all(
            db,
            event_id,
            registration_status
        )

    @staticmethod
    def cancel_registration(
        db: Session,
        registration_id: int
    ):
        registration = RegistrationService.get_registration(
            db,
            registration_id
        )

        if registration.registration_status == RegistrationStatus.CANCELLED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration is already cancelled"
            )

        if registration.registration_status == RegistrationStatus.ATTENDED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Attended registration cannot be cancelled"
            )

        return RegistrationRepository.update(
            db,
            registration,
            {
                "registration_status":
                RegistrationStatus.CANCELLED
            }
        )