from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.event import Event
from app.repositories.event_repository import EventRepository
from app.schemas.event import EventCreate, EventUpdate


class EventService:

    @staticmethod
    def validate_dates(
        start_date,
        end_date,
        registration_start,
        registration_end
    ):
        if end_date <= start_date:
            raise HTTPException(
                status_code=400,
                detail="End date must be after start date"
            )

        if registration_end > start_date:
            raise HTTPException(
                status_code=400,
                detail="Registration closing date cannot be after event start date"
            )

        if registration_start > registration_end:
            raise HTTPException(
                status_code=400,
                detail="Registration start cannot be after registration end"
            )

    @staticmethod
    def create_event(
        db: Session,
        data: EventCreate,
        organizer_id: int
    ):
        EventService.validate_dates(
            data.start_date,
            data.end_date,
            data.registration_start,
            data.registration_end
        )

        event = Event(
            event_name=data.event_name,
            description=data.description,
            event_type=data.event_type,
            organizer_id=organizer_id,
            city=data.city,
            start_date=data.start_date,
            end_date=data.end_date,
            registration_start=data.registration_start,
            registration_end=data.registration_end,
            capacity=data.capacity,
            status=data.status
        )

        return EventRepository.create(
            db,
            event
        )

    @staticmethod
    def update_event(
        db: Session,
        event_id: int,
        data: EventUpdate,
        current_user
    ):
        event = EventRepository.get_by_id(
            db,
            event_id
        )

        if not event:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        if (
            current_user.role != "ADMIN"
            and event.organizer_id != current_user.id
        ):
            raise HTTPException(
                status_code=403,
                detail="You can update only your own events"
            )

        update_data = data.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(event, key, value)

        EventService.validate_dates(
            event.start_date,
            event.end_date,
            event.registration_start,
            event.registration_end
        )

        return EventRepository.update(
            db,
            event
        )

    @staticmethod
    def delete_event(
        db: Session,
        event_id: int,
        current_user
    ):
        event = EventRepository.get_by_id(
            db,
            event_id
        )

        if not event:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        if (
            current_user.role != "ADMIN"
            and event.organizer_id != current_user.id
        ):
            raise HTTPException(
                status_code=403,
                detail="You can delete only your own events"
            )

        return EventRepository.delete(
            db,
            event
        )