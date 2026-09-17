from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.attendee import (
    AttendeeCreate,
    AttendeeResponse,
    AttendeeUpdate
)
from app.services.attendee_service import AttendeeService
from app.utils.dependencies import require_roles
from app.utils.enums import UserRole


router = APIRouter(
    prefix="/attendees",
    tags=["Attendees"]
)


@router.post(
    "",
    response_model=AttendeeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_attendee(
    data: AttendeeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.EVENT_ORGANIZER,
            UserRole.STAFF
        )
    )
):
    return AttendeeService.create_attendee(
        db,
        data
    )


@router.get(
    "",
    response_model=list[AttendeeResponse]
)
def get_attendees(
    db: Session = Depends(get_db)
):
    return AttendeeService.get_attendees(db)


@router.get(
    "/{attendee_id}",
    response_model=AttendeeResponse
)
def get_attendee(
    attendee_id: int,
    db: Session = Depends(get_db)
):
    return AttendeeService.get_attendee(
        db,
        attendee_id
    )


@router.put(
    "/{attendee_id}",
    response_model=AttendeeResponse
)
def update_attendee(
    attendee_id: int,
    data: AttendeeUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.EVENT_ORGANIZER,
            UserRole.STAFF
        )
    )
):
    return AttendeeService.update_attendee(
        db,
        attendee_id,
        data
    )