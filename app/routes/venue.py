from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.venue import Venue
from app.schemas.venue import VenueCreate, VenueUpdate, VenueResponse
from app.utils.dependencies import get_current_user

router = APIRouter(
    prefix="/venues",
    tags=["Venues"]
)


@router.post("", response_model=VenueResponse)
def create_venue(
    data: VenueCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    venue = Venue(
        venue_name=data.venue_name,
        address=data.address,
        city=data.city,
        capacity=data.capacity,
        facilities=data.facilities,
        status=data.status
    )

    db.add(venue)
    db.commit()
    db.refresh(venue)

    return venue


@router.get("", response_model=list[VenueResponse])
def get_venues(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Venue).filter(
        Venue.is_deleted == False
    ).all()


@router.get("/{venue_id}", response_model=VenueResponse)
def get_venue(
    venue_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    venue = db.query(Venue).filter(
        Venue.id == venue_id,
        Venue.is_deleted == False
    ).first()

    if not venue:
        raise HTTPException(
            status_code=404,
            detail="Venue not found"
        )

    return venue


@router.put("/{venue_id}", response_model=VenueResponse)
def update_venue(
    venue_id: int,
    data: VenueUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    venue = db.query(Venue).filter(
        Venue.id == venue_id,
        Venue.is_deleted == False
    ).first()

    if not venue:
        raise HTTPException(
            status_code=404,
            detail="Venue not found"
        )

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(venue, key, value)

    db.commit()
    db.refresh(venue)

    return venue


@router.delete("/{venue_id}")
def delete_venue(
    venue_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    venue = db.query(Venue).filter(
        Venue.id == venue_id,
        Venue.is_deleted == False
    ).first()

    if not venue:
        raise HTTPException(
            status_code=404,
            detail="Venue not found"
        )

    venue.is_deleted = True
    db.commit()

    return {
        "message": "Venue deleted successfully"
    }