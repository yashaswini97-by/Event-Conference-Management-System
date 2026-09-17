from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.purchase import Purchase


class PurchaseRepository:

    @staticmethod
    def create(
        db: Session,
        purchase: Purchase
    ):
        db.add(purchase)
        db.commit()
        db.refresh(purchase)

        return purchase

    @staticmethod
    def get_by_id(
        db: Session,
        purchase_id: int
    ):
        return db.scalar(
            select(Purchase).where(
                Purchase.id == purchase_id
            )
        )

    @staticmethod
    def update(
        db: Session,
        purchase: Purchase,
        data: dict
    ):
        for key, value in data.items():
            setattr(purchase, key, value)

        db.commit()
        db.refresh(purchase)

        return purchase