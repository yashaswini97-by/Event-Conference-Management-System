from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.ticket import (
    TicketCreate,
    TicketResponse,
    TicketUpdate
)
from app.services.ticket_service import TicketService
from app.utils.dependencies import require_roles
from app.utils.enums import UserRole


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


@router.post(
    "",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED
)
def create_ticket(
    data: TicketCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.EVENT_ORGANIZER
        )
    )
):
    return TicketService.create_ticket(
        db,
        data
    )


@router.put(
    "/{ticket_id}",
    response_model=TicketResponse
)
def update_ticket(
    ticket_id: int,
    data: TicketUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.EVENT_ORGANIZER
        )
    )
):
    return TicketService.update_ticket(
        db,
        ticket_id,
        data
    )