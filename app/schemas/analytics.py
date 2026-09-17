from pydantic import BaseModel
from typing import List


class AdminDashboardResponse(BaseModel):
    total_events: int
    active_events: int
    completed_events: int
    total_attendees: int
    total_registrations: int
    tickets_sold: int
    revenue: float
    refunds: float
    average_event_rating: float


class OrganizerDashboardResponse(BaseModel):
    total_registrations: int
    tickets_sold: int
    revenue: float
    attendance: int
    session_bookings: int


class DailyRegistrationReport(BaseModel):
    date: str
    registrations: int


class EventRevenueReport(BaseModel):
    event_id: int
    event_name: str
    revenue: float


class TicketSalesReport(BaseModel):
    event_id: int
    event_name: str
    tickets_sold: int


class AttendanceReport(BaseModel):
    event_id: int
    event_name: str
    attendance: int


class SpeakerRatingReport(BaseModel):
    speaker_id: int
    speaker_name: str
    average_rating: float
    feedback_count: int


class SessionPopularityReport(BaseModel):
    session_id: int
    session_title: str
    bookings: int


class AdminReportsResponse(BaseModel):
    daily_registrations: List[DailyRegistrationReport]
    event_revenue: List[EventRevenueReport]
    ticket_sales: List[TicketSalesReport]
    attendance: List[AttendanceReport]
    speaker_ratings: List[SpeakerRatingReport]
    session_popularity: List[SessionPopularityReport]


class OrganizerReportsResponse(BaseModel):
    daily_registrations: List[DailyRegistrationReport]
    event_revenue: List[EventRevenueReport]
    ticket_sales: List[TicketSalesReport]
    attendance: List[AttendanceReport]
    speaker_ratings: List[SpeakerRatingReport]
    session_popularity: List[SessionPopularityReport]