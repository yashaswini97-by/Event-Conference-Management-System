from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.purchase import PurchaseCreate, PurchaseResponse
from app.services.purchase_service import PurchaseService

router = APIRouter(
    prefix="/purchases",
    tags=["Purchases"]
)


@router.post(
    "",
    response_model=PurchaseResponse,
    status_code=status.HTTP_201_CREATED
)
def create_purchase(
    data: PurchaseCreate,
    db: Session = Depends(get_db)
):
    return PurchaseService.create_purchase(
        db,
        data
    )


@router.get(
    "/{purchase_id}",
    response_model=PurchaseResponse
)
def get_purchase(
    purchase_id: int,
    db: Session = Depends(get_db)
):
    return PurchaseService.get_purchase(
        db,
        purchase_id
    )