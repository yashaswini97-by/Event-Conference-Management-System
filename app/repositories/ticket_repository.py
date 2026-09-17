from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ticket import Ticket


class TicketRepository:

    @staticmethod
    def create(
        db: Session,
        ticket: Ticket
    ):
        db.add(ticket)
        db.commit()
        db.refresh(ticket)

        return ticket

    @staticmethod
    def get_by_id(
        db: Session,
        ticket_id: int
    ):
        return db.scalar(
            select(Ticket).where(
                Ticket.id == ticket_id
            )
        )

    @staticmethod
    def get_by_event(
        db: Session,
        event_id: int
    ):
        return db.scalars(
            select(Ticket)
            .where(
                Ticket.event_id == event_id
            )
            .order_by(Ticket.id.desc())
        ).all()

    @staticmethod
    def update(
        db: Session,
        ticket: Ticket,
        data: dict
    ):
        for key, value in data.items():
            setattr(ticket, key, value)

        db.commit()
        db.refresh(ticket)

        return ticket