from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.hall import Hall
from app.models.venue import Venue
from app.repositories.hall_repository import HallRepository
from app.repositories.venue_repository import VenueRepository
from app.schemas.venue import HallCreate, VenueCreate


class VenueService:

    @staticmethod
    def create_venue(
        db: Session,
        data: VenueCreate
    ):
        venue = Venue(
            venue_name=data.venue_name,
            address=data.address,
            city=data.city,
            capacity=data.capacity,
            facilities=data.facilities,
            status=data.status
        )

        return VenueRepository.create(
            db,
            venue
        )

    @staticmethod
    def create_hall(
        db: Session,
        venue_id: int,
        data: HallCreate
    ):
        venue = VenueRepository.get_by_id(
            db,
            venue_id
        )

        if not venue:
            raise HTTPException(
                status_code=404,
                detail="Venue not found"
            )

        if data.capacity > venue.capacity:
            raise HTTPException(
                status_code=400,
                detail="Hall capacity cannot exceed venue capacity"
            )

        hall = Hall(
            venue_id=venue_id,
            hall_name=data.hall_name,
            capacity=data.capacity,
            floor=data.floor,
            availability_status=data.availability_status
        )

        return HallRepository.create(
            db,
            hall
        )

    @staticmethod
    def get_halls(
        db: Session,
        venue_id: int
    ):
        venue = VenueRepository.get_by_id(
            db,
            venue_id
        )

        if not venue:
            raise HTTPException(
                status_code=404,
                detail="Venue not found"
            )

        return HallRepository.get_all_by_venue(
            db,
            venue_id
        )