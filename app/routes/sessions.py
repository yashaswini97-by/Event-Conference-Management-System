from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.session import (
    SessionCreate,
    SessionResponse,
    SessionUpdate
)
from app.services.session_service import SessionService
from app.utils.dependencies import require_roles
from app.utils.enums import UserRole


router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"]
)


@router.post(
    "",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED
)
def create_session(
    data: SessionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.EVENT_ORGANIZER
        )
    )
):
    return SessionService.create_session(
        db,
        data
    )


@router.get(
    "/{session_id}",
    response_model=SessionResponse
)
def get_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    return SessionService.get_session(
        db,
        session_id
    )


@router.put(
    "/{session_id}",
    response_model=SessionResponse
)
def update_session(
    session_id: int,
    data: SessionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.EVENT_ORGANIZER
        )
    )
):
    return SessionService.update_session(
        db,
        session_id,
        data
    )


@router.delete(
    "/{session_id}"
)
def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.EVENT_ORGANIZER
        )
    )
):
    SessionService.delete_session(
        db,
        session_id
    )

    return {
        "message": "Session deleted successfully"
    }