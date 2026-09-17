from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.speaker import (
    SpeakerCreate,
    SpeakerResponse,
    SpeakerStatusResponse,
    SpeakerUpdate
)
from app.services.speaker_service import SpeakerService
from app.utils.dependencies import require_roles
from app.utils.enums import UserRole


router = APIRouter(
    prefix="/speakers",
    tags=["Speakers"]
)


@router.post(
    "",
    response_model=SpeakerResponse,
    status_code=status.HTTP_201_CREATED
)
def create_speaker(
    data: SpeakerCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.EVENT_ORGANIZER
        )
    )
):
    return SpeakerService.create_speaker(
        db,
        data
    )


@router.get(
    "",
    response_model=list[SpeakerResponse]
)
def get_speakers(
    db: Session = Depends(get_db)
):
    return SpeakerService.get_speakers(db)


@router.get(
    "/{speaker_id}",
    response_model=SpeakerResponse
)
def get_speaker(
    speaker_id: int,
    db: Session = Depends(get_db)
):
    return SpeakerService.get_speaker(
        db,
        speaker_id
    )


@router.put(
    "/{speaker_id}",
    response_model=SpeakerResponse
)
def update_speaker(
    speaker_id: int,
    data: SpeakerUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.EVENT_ORGANIZER
        )
    )
):
    return SpeakerService.update_speaker(
        db,
        speaker_id,
        data
    )


@router.delete(
    "/{speaker_id}"
)
def delete_speaker(
    speaker_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    )
):
    SpeakerService.delete_speaker(
        db,
        speaker_id
    )

    return {
        "message": "Speaker deleted successfully"
    }


@router.patch(
    "/{speaker_id}/activate",
    response_model=SpeakerStatusResponse
)
def activate_speaker(
    speaker_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    )
):
    speaker = SpeakerService.activate_speaker(
        db,
        speaker_id
    )

    return {
        "message": "Speaker activated successfully",
        "speaker_id": speaker.id,
        "is_active": speaker.is_active
    }


@router.patch(
    "/{speaker_id}/deactivate",
    response_model=SpeakerStatusResponse
)
def deactivate_speaker(
    speaker_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    )
):
    speaker = SpeakerService.deactivate_speaker(
        db,
        speaker_id
    )

    return {
        "message": "Speaker deactivated successfully",
        "speaker_id": speaker.id,
        "is_active": speaker.is_active
    }