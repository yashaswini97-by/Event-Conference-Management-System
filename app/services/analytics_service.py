from sqlalchemy.orm import Session

from app.repositories.analytics_repository import AnalyticsRepository


class AnalyticsService:

    def __init__(self):
        self.repo = AnalyticsRepository()

    def get_admin_dashboard(self, db: Session):

        return {
            "total_events": self.repo.get_total_events(db),
            "active_events": self.repo.get_active_events(db),
            "completed_events": self.repo.get_completed_events(db),
            "total_attendees": self.repo.get_total_attendees(db),
            "total_registrations": self.repo.get_total_registrations(db),
            "tickets_sold": self.repo.get_total_tickets_sold(db),
            "revenue": self.repo.get_total_revenue(db),

            # Refunds will be connected in Level 16.
            "refunds": 0.0,

            "average_event_rating":
                self.repo.get_average_rating(db),
        }

    def get_organizer_dashboard(
        self,
        db: Session,
        organizer_id: int
    ):

        return {
            "total_registrations":
                self.repo.get_organizer_registrations(
                    db,
                    organizer_id
                ),

            "tickets_sold":
                self.repo.get_organizer_tickets_sold(
                    db,
                    organizer_id
                ),

            "revenue":
                self.repo.get_organizer_revenue(
                    db,
                    organizer_id
                ),

            "attendance":
                self.repo.get_organizer_attendance(
                    db,
                    organizer_id
                ),

            "session_bookings":
                self.repo.get_organizer_session_bookings(
                    db,
                    organizer_id
                ),
        }

    def get_reports(
        self,
        db: Session,
        organizer_id=None
    ):

        daily = self.repo.daily_registrations(
            db,
            organizer_id
        )

        revenue = self.repo.event_revenue(
            db,
            organizer_id
        )

        tickets = self.repo.ticket_sales(
            db,
            organizer_id
        )

        attendance = self.repo.attendance(
            db,
            organizer_id
        )

        speakers = self.repo.speaker_ratings(
            db,
            organizer_id
        )

        sessions = self.repo.session_popularity(
            db,
            organizer_id
        )

        return {
            "daily_registrations": [
                {
                    "date": str(row.date),
                    "registrations": row.registrations
                }
                for row in daily
            ],

            "event_revenue": [
                {
                    "event_id": row.id,
                    "event_name": row.event_name,
                    "revenue": float(row.revenue or 0)
                }
                for row in revenue
            ],

            "ticket_sales": [
                {
                    "event_id": row.id,
                    "event_name": row.event_name,
                    "tickets_sold": int(row.tickets_sold or 0)
                }
                for row in tickets
            ],

            "attendance": [
                {
                    "event_id": row.id,
                    "event_name": row.event_name,
                    "attendance": row.attendance
                }
                for row in attendance
            ],

            "speaker_ratings": [
                {
                    "speaker_id": row.id,
                    "speaker_name": row.name,
                    "average_rating":
                        round(float(row.average_rating or 0), 2),
                    "feedback_count": row.feedback_count
                }
                for row in speakers
            ],

            "session_popularity": [
                {
                    "session_id": row.id,
                    "session_title": row.title,
                    "bookings": row.bookings
                }
                for row in sessions
            ]
        }