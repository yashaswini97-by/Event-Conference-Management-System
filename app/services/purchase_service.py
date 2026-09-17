from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.purchase import Purchase
from app.models.registration import Registration
from app.models.ticket import Ticket

from app.repositories.purchase_repository import PurchaseRepository
from app.repositories.registration_repository import RegistrationRepository
from app.services.ticket_service import TicketService

from app.schemas.purchase import PurchaseCreate
from app.utils.enums import PurchaseStatus, RegistrationStatus


TAX_RATE = 0.05


class PurchaseService:

    @staticmethod
    def create_purchase(
        db: Session,
        ticket_id: int,
        data: PurchaseCreate
    ):

        # 1. Validate registration
        registration = RegistrationRepository.get_by_id(
            db,
            data.registration_id
        )

        if not registration:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registration not found"
            )

        if registration.registration_status == RegistrationStatus.CANCELLED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cancelled registration cannot purchase tickets"
            )

        if registration.registration_status == RegistrationStatus.ATTENDED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Attended registration cannot purchase tickets"
            )

        # 2. Validate ticket
        ticket = TicketService.validate_purchase(
            db,
            ticket_id,
            data.quantity
        )

        # 3. Make sure ticket belongs to same event
        if ticket.event_id != registration.event_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ticket does not belong to registration event"
            )

        # 4. Calculate amount
        subtotal = ticket.price * data.quantity

        discount = 0.0

        # Simple coupon example
        if data.coupon_code == "EARLY10":
            discount = subtotal * 0.10

        taxable_amount = subtotal - discount

        tax = taxable_amount * TAX_RATE

        total_amount = taxable_amount + tax

        # Round money values
        subtotal = round(subtotal, 2)
        discount = round(discount, 2)
        tax = round(tax, 2)
        total_amount = round(total_amount, 2)

        # 5. Reduce ticket availability
        ticket.available_quantity -= data.quantity

        purchase = Purchase(
            registration_id=data.registration_id,
            ticket_id=ticket_id,
            quantity=data.quantity,
            subtotal=subtotal,
            discount=discount,
            tax=tax,
            total_amount=total_amount,
            status=PurchaseStatus.PENDING
        )

        db.add(purchase)
        db.commit()
        db.refresh(purchase)

        return purchase

    @staticmethod
    def get_purchase(
        db: Session,
        purchase_id: int
    ):
        purchase = PurchaseRepository.get_by_id(
            db,
            purchase_id
        )

        if not purchase:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Purchase not found"
            )

        return purchase