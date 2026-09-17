from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.utils.enums import PaymentMethod, PaymentStatus


class PaymentCreate(BaseModel):
    transaction_id: str = Field(
        ...,
        min_length=3,
        max_length=150
    )

    payment_method: PaymentMethod

    amount: float = Field(
        ...,
        ge=0
    )

    payment_status: PaymentStatus


class PaymentResponse(BaseModel):
    id: int
    purchase_id: int
    transaction_id: str
    payment_method: PaymentMethod
    amount: float
    payment_status: PaymentStatus
    payment_date: datetime

    model_config = ConfigDict(
        from_attributes=True
    )