from sqlalchemy.orm import Session

from app.models.hall import Hall


class HallRepository:

    @staticmethod
    def create(
        db: Session,
        hall: Hall
    ):
        db.add(hall)
        db.commit()
        db.refresh(hall)

        return hall

    @staticmethod
    def get_all_by_venue(
        db: Session,
        venue_id: int
    ):
        return (
            db.query(Hall)
            .filter(
                Hall.venue_id == venue_id,
                Hall.is_deleted == False
            )
            .order_by(Hall.id.desc())
            .all()
        )