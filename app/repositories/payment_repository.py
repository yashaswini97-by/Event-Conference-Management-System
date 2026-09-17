from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.payment import Payment


class PaymentRepository:

    @staticmethod
    def create(
        db: Session,
        payment: Payment
    ):
        db.add(payment)
        db.commit()
        db.refresh(payment)

        return payment

    @staticmethod
    def get_by_id(
        db: Session,
        payment_id: int
    ):
        return db.scalar(
            select(Payment).where(
                Payment.id == payment_id
            )
        )

    @staticmethod
    def get_by_transaction_id(
        db: Session,
        transaction_id: str
    ):
        return db.scalar(
            select(Payment).where(
                Payment.transaction_id == transaction_id
            )
        )

    @staticmethod
    def get_by_purchase_id(
        db: Session,
        purchase_id: int
    ):
        return db.scalar(
            select(Payment).where(
                Payment.purchase_id == purchase_id
            )
        )