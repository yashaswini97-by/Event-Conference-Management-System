from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.event import Event
from app.models.ticket import Ticket
from app.repositories.ticket_repository import TicketRepository
from app.schemas.ticket import TicketCreate, TicketUpdate


class TicketService:

    @staticmethod
    def validate_event(
        db: Session,
        event_id: int
    ):
        event = db.get(
            Event,
            event_id
        )

        if not event or event.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )

        return event

    @staticmethod
    def validate_dates(
        sale_start,
        sale_end
    ):
        if sale_end <= sale_start:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ticket sale end must be after sale start"
            )

    @staticmethod
    def create_ticket(
        db: Session,
        event_id: int,
        data: TicketCreate
    ):
        event = TicketService.validate_event(
            db,
            event_id
        )

        TicketService.validate_dates(
            data.sale_start,
            data.sale_end
        )

        if data.quantity < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity cannot be negative"
            )

        available_quantity = (
            data.quantity
            if data.available_quantity is None
            else data.available_quantity
        )

        if available_quantity < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Available quantity cannot be negative"
            )

        if available_quantity > data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Available quantity cannot exceed total quantity"
            )

        if data.sale_end > event.start_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ticket sale must end before event starts"
            )

        ticket = Ticket(
            event_id=event_id,
            ticket_type=data.ticket_type,
            price=data.price,
            quantity=data.quantity,
            available_quantity=available_quantity,
            sale_start=data.sale_start,
            sale_end=data.sale_end
        )

        return TicketRepository.create(
            db,
            ticket
        )

    @staticmethod
    def get_ticket(
        db: Session,
        ticket_id: int
    ):
        ticket = TicketRepository.get_by_id(
            db,
            ticket_id
        )

        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found"
            )

        return ticket

    @staticmethod
    def get_event_tickets(
        db: Session,
        event_id: int
    ):
        TicketService.validate_event(
            db,
            event_id
        )

        return TicketRepository.get_by_event(
            db,
            event_id
        )

    @staticmethod
    def update_ticket(
        db: Session,
        ticket_id: int,
        data: TicketUpdate
    ):
        ticket = TicketService.get_ticket(
            db,
            ticket_id
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        sale_start = update_data.get(
            "sale_start",
            ticket.sale_start
        )

        sale_end = update_data.get(
            "sale_end",
            ticket.sale_end
        )

        quantity = update_data.get(
            "quantity",
            ticket.quantity
        )

        available_quantity = update_data.get(
            "available_quantity",
            ticket.available_quantity
        )

        TicketService.validate_dates(
            sale_start,
            sale_end
        )

        if quantity < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity cannot be negative"
            )

        if available_quantity < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Available quantity cannot be negative"
            )

        if available_quantity > quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Available quantity cannot exceed total quantity"
            )

        event = TicketService.validate_event(
            db,
            ticket.event_id
        )

        if sale_end > event.start_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ticket sale must end before event starts"
            )

        return TicketRepository.update(
            db,
            ticket,
            update_data
        )

    @staticmethod
    def validate_purchase(
        db: Session,
        ticket_id: int,
        quantity: int
    ):
        ticket = TicketService.get_ticket(
            db,
            ticket_id
        )

        now = datetime.utcnow()

        if now < ticket.sale_start:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ticket sales have not started"
            )

        if now > ticket.sale_end:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ticket sales have ended"
            )

        if quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Purchase quantity must be greater than zero"
            )

        if quantity > ticket.available_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough tickets available"
            )

        return ticket