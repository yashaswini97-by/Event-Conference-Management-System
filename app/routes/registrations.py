from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.registration import (
    RegistrationCreate,
    RegistrationResponse
)
from app.services.registration_service import RegistrationService
from app.utils.dependencies import require_roles
from app.utils.enums import UserRole


router = APIRouter(
    prefix="/registrations",
    tags=["Registrations"]
)


@router.get(
    "",
    response_model=list[RegistrationResponse]
)
def get_registrations(
    event_id: int | None = None,
    registration_status: str | None = None,
    db: Session = Depends(get_db)
):
    return RegistrationService.get_registrations(
        db,
        event_id,
        registration_status
    )


@router.get(
    "/{registration_id}",
    response_model=RegistrationResponse
)
def get_registration(
    registration_id: int,
    db: Session = Depends(get_db)
):
    return RegistrationService.get_registration(
        db,
        registration_id
    )


@router.post(
    "/{registration_id}/cancel",
    response_model=RegistrationResponse
)
def cancel_registration(
    registration_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.EVENT_ORGANIZER,
            UserRole.STAFF,
            UserRole.ATTENDEE
        )
    )
):
    return RegistrationService.cancel_registration(
        db,
        registration_id
    )