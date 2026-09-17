from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.utils.enums import RefundReason, RefundStatus


class RefundCreate(BaseModel):
    payment_id: int
    reason: RefundReason
    remarks: Optional[str] = None


class RefundResponse(BaseModel):
    id: int
    payment_id: int
    purchase_id: int
    amount: float
    reason: RefundReason
    status: RefundStatus
    remarks: Optional[str]
    requested_at: datetime
    processed_at: Optional[datetime]
    processed_by: Optional[int]

    class Config:
        from_attributes = True


class RefundAction(BaseModel):
    remarks: Optional[str] = None