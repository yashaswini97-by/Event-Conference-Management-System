from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# =========================
# Database
# =========================
from app.database import Base, engine


# =========================
# Models
# =========================
from app.models.user import User
from app.models.event import Event
from app.models.venue import Venue
from app.models.hall import Hall
from app.models.speaker import Speaker
from app.models.session import SessionModel
from app.models.attendee import Attendee
from app.models.registration import Registration
from app.models.ticket import Ticket
from app.models.purchase import Purchase
from app.models.payment import Payment
from app.models.session_booking import SessionBooking
from app.models.checkin import CheckIn
from app.models.certificate import Certificate
from app.models.feedback import Feedback
from app.models.notification import Notification
from app.models.refund import Refund
from app.models.audit_log import AuditLog


# =========================
# Routes
# =========================
from app.routes import (
    auth,
    events,
    venue,
    speakers,
    sessions,
    attendees,
    registrations,
    tickets,
    purchases,
    payments,
    bookings,
    chekin,
    certificates,
    feedback,
    notifications,
    analytics,
    refunds,
    audit,
    reports,
)


# =========================
# Create Database Tables
# =========================
Base.metadata.create_all(bind=engine)


# =========================
# FastAPI Application
# =========================
app = FastAPI(
    title="Event & Conference Management System",
    description="Advanced Backend Event & Conference Management System",
    version="1.0.0",
)


# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# Root
# =========================
@app.get("/")
def root():
    return {
        "message": "Event & Conference Management System API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


# =========================
# Health Check
# =========================
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "Event & Conference Management System",
    }


# =========================
# API Prefix
# =========================
API_PREFIX = "/api/v1"


# =========================
# Include Routers
# =========================

app.include_router(
    auth.router,
    prefix=API_PREFIX,
)

app.include_router(
    events.router,
    prefix=API_PREFIX,
)

app.include_router(
    venue.router,
    prefix=API_PREFIX,
)

app.include_router(
    speakers.router,
    prefix=API_PREFIX,
)

app.include_router(
    sessions.router,
    prefix=API_PREFIX,
)

app.include_router(
    attendees.router,
    prefix=API_PREFIX,
)

app.include_router(
    registrations.router,
    prefix=API_PREFIX,
)

app.include_router(
    tickets.router,
    prefix=API_PREFIX,
)

app.include_router(
    purchases.router,
    prefix=API_PREFIX,
)

app.include_router(
    payments.router,
    prefix=API_PREFIX,
)

app.include_router(
    bookings.router,
    prefix=API_PREFIX,
)

app.include_router(
    chekin.router,
    prefix=API_PREFIX,
)

app.include_router(
    certificates.router,
    prefix=API_PREFIX,
)

app.include_router(
    feedback.router,
    prefix=API_PREFIX,
)

app.include_router(
    notifications.router,
    prefix=API_PREFIX,
)

app.include_router(
    analytics.router,
    prefix=API_PREFIX,
)

app.include_router(
    refunds.router,
    prefix=API_PREFIX,
)

app.include_router(
    audit.router,
    prefix=API_PREFIX,
)

app.include_router(
    reports.router,
    prefix=API_PREFIX,
)