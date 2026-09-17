from sqlalchemy.orm import Session

from app.models.event import Event


class EventRepository:

    @staticmethod
    def create(
        db: Session,
        event: Event
    ):
        db.add(event)
        db.commit()
        db.refresh(event)

        return event

    @staticmethod
    def get_by_id(
        db: Session,
        event_id: int
    ):
        return (
            db.query(Event)
            .filter(
                Event.id == event_id,
                Event.is_deleted == False
            )
            .first()
        )

    @staticmethod
    def get_all(
        db: Session,
        event_type=None,
        city=None,
        status=None,
        start_date=None,
        end_date=None,
        page=1,
        limit=10,
        sort_by="created_at",
        sort_order="desc"
    ):
        query = db.query(Event).filter(
            Event.is_deleted == False
        )

        if event_type:
            query = query.filter(
                Event.event_type == event_type
            )

        if city:
            query = query.filter(
                Event.city.ilike(f"%{city}%")
            )

        if status:
            query = query.filter(
                Event.status == status
            )

        if start_date:
            query = query.filter(
                Event.start_date >= start_date
            )

        if end_date:
            query = query.filter(
                Event.start_date <= end_date
            )

        allowed_sort_fields = {
            "created_at": Event.created_at,
            "start_date": Event.start_date,
            "event_name": Event.event_name,
            "capacity": Event.capacity
        }

        sort_column = allowed_sort_fields.get(
            sort_by,
            Event.created_at
        )

        if sort_order.lower() == "asc":
            query = query.order_by(
                sort_column.asc()
            )
        else:
            query = query.order_by(
                sort_column.desc()
            )

        offset = (page - 1) * limit

        return query.offset(offset).limit(limit).all()

    @staticmethod
    def update(
        db: Session,
        event: Event
    ):
        db.commit()
        db.refresh(event)

        return event

    @staticmethod
    def delete(
        db: Session,
        event: Event
    ):
        event.is_deleted = True

        db.commit()

        return event