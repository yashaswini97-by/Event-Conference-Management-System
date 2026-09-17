from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.repositories.event_repository import EventRepository
from app.schemas.event import (
    EventCreate,
    EventResponse,
    EventUpdate,
)
from app.services.event_service import EventService
from app.utils.dependencies import (
    get_current_user,
    require_roles,
)
from app.utils.enums import (
    EventStatus,
    EventType,
    UserRole,
)


router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


@router.post(
    "",
    response_model=EventResponse,
    status_code=201
)
def create_event(
    data: EventCreate,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.EVENT_ORGANIZER
        )
    ),
    db: Session = Depends(get_db)
):
    return EventService.create_event(
        db,
        data,
        current_user.id
    )


@router.get(
    "",
    response_model=list[EventResponse]
)
def get_events(
    event_type: EventType | None = None,
    city: str | None = None,
    status: EventStatus | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    sort_by: str = "created_at",
    sort_order: str = "desc",
    db: Session = Depends(get_db)
):
    return EventRepository.get_all(
        db=db,
        event_type=event_type,
        city=city,
        status=status,
        start_date=start_date,
        end_date=end_date,
        page=page,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order
    )


@router.get(
    "/{event_id}",
    response_model=EventResponse
)
def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    event = EventRepository.get_by_id(
        db,
        event_id
    )

    if not event:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return event


@router.put(
    "/{event_id}",
    response_model=EventResponse
)
def update_event(
    event_id: int,
    data: EventUpdate,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.EVENT_ORGANIZER
        )
    ),
    db: Session = Depends(get_db)
):
    return EventService.update_event(
        db,
        event_id,
        data,
        current_user
    )


@router.delete(
    "/{event_id}"
)
def delete_event(
    event_id: int,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.EVENT_ORGANIZER
        )
    ),
    db: Session = Depends(get_db)
):
    EventService.delete_event(
        db,
        event_id,
        current_user
    )

    return {
        "message": "Event deleted successfully"
    }