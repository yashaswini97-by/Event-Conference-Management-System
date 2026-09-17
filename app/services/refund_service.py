from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.refund import Refund
from app.models.payment import Payment
from app.models.purchase import Purchase
from app.models.registration import Registration
from app.models.event import Event

from app.repositories.refund_repository import RefundRepository

from app.utils.enums import (
    PaymentStatus,
    PurchaseStatus,
    RefundStatus,
    RegistrationStatus,
)


class RefundService:

    def __init__(self):
        self.repo = RefundRepository()

    def request_refund(
        self,
        db: Session,
        payment_id: int,
        reason,
        remarks=None,
    ):

        payment = db.query(Payment).filter(
            Payment.id == payment_id
        ).first()

        if not payment:
            raise HTTPException(
                status_code=404,
                detail="Payment not found",
            )

        if payment.payment_status != PaymentStatus.SUCCESS:
            raise HTTPException(
                status_code=400,
                detail="Only successful payments can be refunded",
            )

        existing = self.repo.get_by_payment(
            db,
            payment_id,
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Refund already requested for this payment",
            )

        purchase = db.query(Purchase).filter(
            Purchase.id == payment.purchase_id
        ).first()

        if not purchase:
            raise HTTPException(
                status_code=404,
                detail="Purchase not found",
            )

        if purchase.status != PurchaseStatus.COMPLETED:
            raise HTTPException(
                status_code=400,
                detail="Only completed purchases can be refunded",
            )

        refund = Refund(
            payment_id=payment.id,
            purchase_id=purchase.id,
            amount=payment.amount,
            reason=reason,
            status=RefundStatus.REQUESTED,
            remarks=remarks,
        )

        return self.repo.create(
            db,
            refund,
        )

    def get_refund(
        self,
        db: Session,
        refund_id: int,
    ):

        refund = self.repo.get_by_id(
            db,
            refund_id,
        )

        if not refund:
            raise HTTPException(
                status_code=404,
                detail="Refund not found",
            )

        return refund

    def get_all_refunds(
        self,
        db: Session,
    ):
        return self.repo.get_all(db)

    def approve_refund(
        self,
        db: Session,
        refund_id: int,
        admin_id: int,
        remarks=None,
    ):

        refund = self.get_refund(
            db,
            refund_id,
        )

        if refund.status != RefundStatus.REQUESTED:
            raise HTTPException(
                status_code=400,
                detail="Only requested refunds can be approved",
            )

        refund.status = RefundStatus.COMPLETED
        refund.processed_at = datetime.utcnow()
        refund.processed_by = admin_id

        if remarks:
            refund.remarks = remarks

        return self.repo.update(
            db,
            refund,
        )

    def reject_refund(
        self,
        db: Session,
        refund_id: int,
        admin_id: int,
        remarks=None,
    ):

        refund = self.get_refund(
            db,
            refund_id,
        )

        if refund.status != RefundStatus.REQUESTED:
            raise HTTPException(
                status_code=400,
                detail="Only requested refunds can be rejected",
            )

        refund.status = RefundStatus.REJECTED
        refund.processed_at = datetime.utcnow()
        refund.processed_by = admin_id

        if remarks:
            refund.remarks = remarks

        return self.repo.update(
            db,
            refund,
        )