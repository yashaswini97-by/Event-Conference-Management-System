from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.utils.enums import TicketType


class TicketCreate(BaseModel):
    ticket_type: TicketType

    price: float = Field(
        ...,
        ge=0
    )

    quantity: int = Field(
        ...,
        ge=0
    )

    available_quantity: int | None = None

    sale_start: datetime
    sale_end: datetime


class TicketUpdate(BaseModel):
    ticket_type: TicketType | None = None

    price: float | None = Field(
        default=None,
        ge=0
    )

    quantity: int | None = Field(
        default=None,
        ge=0
    )

    available_quantity: int | None = Field(
        default=None,
        ge=0
    )

    sale_start: datetime | None = None

    sale_end: datetime | None = None


class TicketResponse(BaseModel):
    id: int
    event_id: int
    ticket_type: TicketType
    price: float
    quantity: int
    available_quantity: int
    sale_start: datetime
    sale_end: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )