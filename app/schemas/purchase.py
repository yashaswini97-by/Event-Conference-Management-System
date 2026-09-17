from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.utils.enums import PurchaseStatus


class PurchaseCreate(BaseModel):
    registration_id: int

    quantity: int = Field(
        ...,
        gt=0
    )

    coupon_code: str | None = None


class PurchaseResponse(BaseModel):
    id: int
    registration_id: int
    ticket_id: int
    quantity: int
    subtotal: float
    discount: float
    tax: float
    total_amount: float
    status: PurchaseStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )