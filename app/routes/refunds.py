from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.refund import (
    RefundCreate,
    RefundResponse,
    RefundAction,
)

from app.services.refund_service import RefundService

from app.utils.dependencies import (
    get_current_user,
    require_roles,
)

from app.utils.enums import UserRole


router = APIRouter(
    prefix="/refunds",
    tags=["Refunds"],
)

service = RefundService()


@router.post(
    "",
    response_model=RefundResponse,
)
def request_refund(
    data: RefundCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return service.request_refund(
        db,
        data.payment_id,
        data.reason,
        data.remarks,
    )


@router.get(
    "",
    response_model=List[RefundResponse],
)
def get_refunds(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
):

    return service.get_all_refunds(db)


@router.get(
    "/{refund_id}",
    response_model=RefundResponse,
)
def get_refund(
    refund_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return service.get_refund(
        db,
        refund_id,
    )


@router.post(
    "/{refund_id}/approve",
    response_model=RefundResponse,
)
def approve_refund(
    refund_id: int,
    data: RefundAction,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
):

    return service.approve_refund(
        db,
        refund_id,
        current_user.id,
        data.remarks,
    )


@router.post(
    "/{refund_id}/reject",
    response_model=RefundResponse,
)
def reject_refund(
    refund_id: int,
    data: RefundAction,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
):

    return service.reject_refund(
        db,
        refund_id,
        current_user.id,
        data.remarks,
    )