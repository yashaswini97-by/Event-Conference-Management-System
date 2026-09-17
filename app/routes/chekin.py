from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.checkin import (
    CheckInCreate,
    CheckInResponse,
    AttendanceResponse
)

from app.services.checkin_service import CheckInService

from app.utils.dependencies import get_current_user


router = APIRouter(
    tags=["Check-in & Attendance"]
)


@router.post(
    "/registrations/{registration_id}/check-in",
    response_model=CheckInResponse
)
def check_in(
    registration_id: int,
    data: CheckInCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return CheckInService.check_in(
        db,
        registration_id,
        data.check_in_method
    )


@router.post(
    "/registrations/{registration_id}/check-out",
    response_model=CheckInResponse
)
def check_out(
    registration_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return CheckInService.check_out(
        db,
        registration_id
    )


@router.get(
    "/events/{event_id}/attendance",
    response_model=list[AttendanceResponse]
)
def get_event_attendance(
    event_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return CheckInService.get_event_attendance(
        db,
        event_id
    )