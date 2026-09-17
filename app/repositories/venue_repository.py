from sqlalchemy.orm import Session

from app.models.venue import Venue


class VenueRepository:

    @staticmethod
    def create(
        db: Session,
        venue: Venue
    ):
        db.add(venue)
        db.commit()
        db.refresh(venue)

        return venue

    @staticmethod
    def get_by_id(
        db: Session,
        venue_id: int
    ):
        return (
            db.query(Venue)
            .filter(
                Venue.id == venue_id,
                Venue.is_deleted == False
            )
            .first()
        )

    @staticmethod
    def get_all(
        db: Session
    ):
        return (
            db.query(Venue)
            .filter(
                Venue.is_deleted == False
            )
            .order_by(Venue.id.desc())
            .all()
        )