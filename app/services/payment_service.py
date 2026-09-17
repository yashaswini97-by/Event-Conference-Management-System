from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.payment import Payment

from app.repositories.payment_repository import PaymentRepository
from app.repositories.purchase_repository import PurchaseRepository
from app.repositories.registration_repository import RegistrationRepository

from app.schemas.payment import PaymentCreate

from app.utils.enums import (
    PaymentStatus,
    PurchaseStatus,
    RegistrationStatus
)


class PaymentService:

    @staticmethod
    def create_payment(
        db: Session,
        purchase_id: int,
        data: PaymentCreate
    ):

        # 1. Check purchase
        purchase = PurchaseRepository.get_by_id(
            db,
            purchase_id
        )

        if not purchase:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Purchase not found"
            )

        # 2. Prevent duplicate successful payment
        existing_purchase_payment = (
            PaymentRepository.get_by_purchase_id(
                db,
                purchase_id
            )
        )

        if existing_purchase_payment:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Payment already exists for this purchase"
            )

        # 3. Duplicate transaction check
        existing_transaction = (
            PaymentRepository.get_by_transaction_id(
                db,
                data.transaction_id
            )
        )

        if existing_transaction:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Transaction ID already exists"
            )

        # 4. Amount validation
        if round(data.amount, 2) != round(
            purchase.total_amount,
            2
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment amount does not match purchase total"
            )

        # 5. Failed payment
        if data.payment_status == PaymentStatus.FAILED:

            payment = Payment(
                purchase_id=purchase_id,
                transaction_id=data.transaction_id,
                payment_method=data.payment_method,
                amount=data.amount,
                payment_status=PaymentStatus.FAILED
            )

            db.add(payment)

            purchase.status = PurchaseStatus.CANCELLED

            db.commit()
            db.refresh(payment)

            return payment

        # 6. Pending payment
        if data.payment_status == PaymentStatus.PENDING:

            payment = Payment(
                purchase_id=purchase_id,
                transaction_id=data.transaction_id,
                payment_method=data.payment_method,
                amount=data.amount,
                payment_status=PaymentStatus.PENDING
            )

            db.add(payment)

            db.commit()
            db.refresh(payment)

            return payment

        # 7. Successful payment
        payment = Payment(
            purchase_id=purchase_id,
            transaction_id=data.transaction_id,
            payment_method=data.payment_method,
            amount=data.amount,
            payment_status=PaymentStatus.SUCCESS
        )

        db.add(payment)

        purchase.status = PurchaseStatus.COMPLETED

        # Successful payment confirms registration
        registration = RegistrationRepository.get_by_id(
            db,
            purchase.registration_id
        )

        if registration:
            registration.registration_status = (
                RegistrationStatus.CONFIRMED
            )

        db.commit()
        db.refresh(payment)

        return payment

    @staticmethod
    def get_payment(
        db: Session,
        payment_id: int
    ):
        payment = PaymentRepository.get_by_id(
            db,
            payment_id
        )

        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )

        return payment