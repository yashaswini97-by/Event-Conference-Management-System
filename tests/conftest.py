import pytest

from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def admin_user():
    return {
        "full_name": "Test Admin",
        "email": "testadmin@example.com",
        "phone": "9876543210",
        "password": "Admin@12345",
        "role": "ADMIN",
    }


@pytest.fixture
def attendee_user():
    return {
        "full_name": "Test Attendee",
        "email": "testattendee@example.com",
        "phone": "9876543211",
        "password": "Attendee@12345",
        "role": "ATTENDEE",
    }