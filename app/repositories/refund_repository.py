from sqlalchemy.orm import Session

from app.models.refund import Refund
from app.utils.enums import RefundStatus


class RefundRepository:

    def create(
        self,
        db: Session,
        refund: Refund,
    ):
        db.add(refund)
        db.commit()
        db.refresh(refund)

        return refund

    def get_by_id(
        self,
        db: Session,
        refund_id: int,
    ):
        return db.query(Refund).filter(
            Refund.id == refund_id
        ).first()

    def get_by_payment(
        self,
        db: Session,
        payment_id: int,
    ):
        return db.query(Refund).filter(
            Refund.payment_id == payment_id
        ).first()

    def get_by_purchase(
        self,
        db: Session,
        purchase_id: int,
    ):
        return db.query(Refund).filter(
            Refund.purchase_id == purchase_id
        ).first()

    def get_all(
        self,
        db: Session,
    ):
        return db.query(
            Refund
        ).order_by(
            Refund.requested_at.desc()
        ).all()

    def get_by_status(
        self,
        db: Session,
        status: RefundStatus,
    ):
        return db.query(Refund).filter(
            Refund.status == status
        ).order_by(
            Refund.requested_at.desc()
        ).all()

    def update(
        self,
        db: Session,
        refund: Refund,
    ):
        db.commit()
        db.refresh(refund)

        return refund