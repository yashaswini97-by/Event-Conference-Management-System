from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.attendee import Attendee
from app.repositories.attendee_repository import AttendeeRepository
from app.schemas.attendee import AttendeeCreate, AttendeeUpdate


class AttendeeService:

    @staticmethod
    def create_attendee(
        db: Session,
        data: AttendeeCreate
    ):
        existing = AttendeeRepository.get_by_email(
            db,
            data.email
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Attendee with this email already exists"
            )

        attendee = Attendee(
            full_name=data.full_name,
            email=data.email,
            phone=data.phone,
            organization=data.organization,
            designation=data.designation
        )

        return AttendeeRepository.create(
            db,
            attendee
        )

    @staticmethod
    def get_attendees(
        db: Session
    ):
        return AttendeeRepository.get_all(db)

    @staticmethod
    def get_attendee(
        db: Session,
        attendee_id: int
    ):
        attendee = AttendeeRepository.get_by_id(
            db,
            attendee_id
        )

        if not attendee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attendee not found"
            )

        return attendee

    @staticmethod
    def update_attendee(
        db: Session,
        attendee_id: int,
        data: AttendeeUpdate
    ):
        attendee = AttendeeService.get_attendee(
            db,
            attendee_id
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "email" in update_data:
            existing = AttendeeRepository.get_by_email(
                db,
                update_data["email"]
            )

            if existing and existing.id != attendee_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Another attendee already uses this email"
                )

        return AttendeeRepository.update(
            db,
            attendee,
            update_data
        )