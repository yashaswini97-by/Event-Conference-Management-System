from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.event import Event
from app.models.attendee import Attendee
from app.models.registration import Registration
from app.models.ticket import Ticket
from app.models.purchase import Purchase
from app.models.checkin import CheckIn
from app.models.feedback import Feedback
from app.models.speaker import Speaker
from app.models.session import SessionModel
from app.models.session_booking import SessionBooking

from app.utils.enums import (
    EventStatus,
    PurchaseStatus,
    RegistrationStatus,
    SessionBookingStatus,
)


class AnalyticsRepository:

    def get_total_events(self, db: Session):
        return db.query(Event).filter(
            Event.is_deleted == False
        ).count()

    def get_active_events(self, db: Session):
        return db.query(Event).filter(
            Event.is_deleted == False,
            Event.status.in_([
                EventStatus.PUBLISHED,
                EventStatus.REGISTRATION_OPEN,
            ])
        ).count()

    def get_completed_events(self, db: Session):
        return db.query(Event).filter(
            Event.is_deleted == False,
            Event.status == EventStatus.COMPLETED
        ).count()

    def get_total_attendees(self, db: Session):
        return db.query(Attendee).count()

    def get_total_registrations(self, db: Session):
        return db.query(Registration).count()

    def get_total_tickets_sold(self, db: Session):
        result = db.query(
            func.coalesce(func.sum(Purchase.quantity), 0)
        ).filter(
            Purchase.status == PurchaseStatus.COMPLETED
        ).scalar()

        return int(result or 0)

    def get_total_revenue(self, db: Session):
        result = db.query(
            func.coalesce(func.sum(Purchase.total_amount), 0)
        ).filter(
            Purchase.status == PurchaseStatus.COMPLETED
        ).scalar()

        return float(result or 0)

    def get_average_rating(self, db: Session):
        result = db.query(
            func.coalesce(func.avg(Feedback.rating), 0)
        ).scalar()

        return round(float(result or 0), 2)

    # -------------------------------
    # Organizer Dashboard
    # -------------------------------

    def get_organizer_registrations(self, db: Session, organizer_id: int):
        return db.query(Registration).join(
            Event,
            Registration.event_id == Event.id
        ).filter(
            Event.organizer_id == organizer_id
        ).count()

    def get_organizer_tickets_sold(self, db: Session, organizer_id: int):
        result = db.query(
            func.coalesce(func.sum(Purchase.quantity), 0)
        ).join(
            Registration,
            Purchase.registration_id == Registration.id
        ).join(
            Event,
            Registration.event_id == Event.id
        ).filter(
            Event.organizer_id == organizer_id,
            Purchase.status == PurchaseStatus.COMPLETED
        ).scalar()

        return int(result or 0)

    def get_organizer_revenue(self, db: Session, organizer_id: int):
        result = db.query(
            func.coalesce(func.sum(Purchase.total_amount), 0)
        ).join(
            Registration,
            Purchase.registration_id == Registration.id
        ).join(
            Event,
            Registration.event_id == Event.id
        ).filter(
            Event.organizer_id == organizer_id,
            Purchase.status == PurchaseStatus.COMPLETED
        ).scalar()

        return float(result or 0)

    def get_organizer_attendance(self, db: Session, organizer_id: int):
        return db.query(CheckIn).join(
            Registration,
            CheckIn.registration_id == Registration.id
        ).join(
            Event,
            Registration.event_id == Event.id
        ).filter(
            Event.organizer_id == organizer_id
        ).count()

    def get_organizer_session_bookings(
        self,
        db: Session,
        organizer_id: int
    ):
        return db.query(SessionBooking).join(
            SessionModel,
            SessionBooking.session_id == SessionModel.id
        ).join(
            Event,
            SessionModel.event_id == Event.id
        ).filter(
            Event.organizer_id == organizer_id,
            SessionBooking.status == SessionBookingStatus.BOOKED
        ).count()

    # -------------------------------
    # Reports
    # -------------------------------

    def daily_registrations(
        self,
        db: Session,
        organizer_id=None
    ):
        query = db.query(
            func.date(Registration.registration_date).label("date"),
            func.count(Registration.id).label("registrations")
        ).join(
            Event,
            Registration.event_id == Event.id
        )

        if organizer_id is not None:
            query = query.filter(
                Event.organizer_id == organizer_id
            )

        return query.group_by(
            func.date(Registration.registration_date)
        ).order_by(
            func.date(Registration.registration_date)
        ).all()

    def event_revenue(
        self,
        db: Session,
        organizer_id=None
    ):
        query = db.query(
            Event.id,
            Event.event_name,
            func.coalesce(
                func.sum(Purchase.total_amount), 0
            ).label("revenue")
        ).join(
            Registration,
            Registration.event_id == Event.id
        ).join(
            Purchase,
            Purchase.registration_id == Registration.id
        ).filter(
            Purchase.status == PurchaseStatus.COMPLETED
        )

        if organizer_id is not None:
            query = query.filter(
                Event.organizer_id == organizer_id
            )

        return query.group_by(
            Event.id,
            Event.event_name
        ).order_by(
            Event.id
        ).all()

    def ticket_sales(
        self,
        db: Session,
        organizer_id=None
    ):
        query = db.query(
            Event.id,
            Event.event_name,
            func.coalesce(
                func.sum(Purchase.quantity), 0
            ).label("tickets_sold")
        ).join(
            Registration,
            Registration.event_id == Event.id
        ).join(
            Purchase,
            Purchase.registration_id == Registration.id
        ).filter(
            Purchase.status == PurchaseStatus.COMPLETED
        )

        if organizer_id is not None:
            query = query.filter(
                Event.organizer_id == organizer_id
            )

        return query.group_by(
            Event.id,
            Event.event_name
        ).order_by(
            Event.id
        ).all()

    def attendance(
        self,
        db: Session,
        organizer_id=None
    ):
        query = db.query(
            Event.id,
            Event.event_name,
            func.count(CheckIn.id).label("attendance")
        ).join(
            Registration,
            Registration.event_id == Event.id
        ).join(
            CheckIn,
            CheckIn.registration_id == Registration.id
        )

        if organizer_id is not None:
            query = query.filter(
                Event.organizer_id == organizer_id
            )

        return query.group_by(
            Event.id,
            Event.event_name
        ).order_by(
            Event.id
        ).all()

    def speaker_ratings(
        self,
        db: Session,
        organizer_id=None
    ):
        query = db.query(
            Speaker.id,
            Speaker.name,
            func.avg(Feedback.rating).label("average_rating"),
            func.count(Feedback.id).label("feedback_count")
        ).join(
            Feedback,
            Feedback.speaker_id == Speaker.id
        ).join(
            Event,
            Feedback.event_id == Event.id
        )

        if organizer_id is not None:
            query = query.filter(
                Event.organizer_id == organizer_id
            )

        return query.group_by(
            Speaker.id,
            Speaker.name
        ).order_by(
            Speaker.id
        ).all()

    def session_popularity(
        self,
        db: Session,
        organizer_id=None
    ):
        query = db.query(
            SessionModel.id,
            SessionModel.title,
            func.count(SessionBooking.id).label("bookings")
        ).join(
            SessionBooking,
            SessionBooking.session_id == SessionModel.id
        ).join(
            Event,
            SessionModel.event_id == Event.id
        ).filter(
            SessionBooking.status == SessionBookingStatus.BOOKED
        )

        if organizer_id is not None:
            query = query.filter(
                Event.organizer_id == organizer_id
            )

        return query.group_by(
            SessionModel.id,
            SessionModel.title
        ).order_by(
            func.count(SessionBooking.id).desc()
        ).all()