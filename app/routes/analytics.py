from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def create_analytics(
    data: dict,
    db: Session = Depends(get_db)
):
    return {
        "message": "Analytics data created successfully",
        "data": data
    }


@router.get("")
def get_analytics(
    db: Session = Depends(get_db)
):
    return {
        "message": "Analytics retrieved successfully"
    }