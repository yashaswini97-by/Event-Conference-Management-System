def get_admin_token(client):

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "testadmin@example.com",
            "password": "Admin@12345",
        },
    )

    return response.json()["access_token"]


def test_get_events(client):

    response = client.get(
        "/api/v1/events"
    )

    assert response.status_code == 200


def test_create_event(client):

    token = get_admin_token(client)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    event_data = {
        "event_name": "Python Technology Conference",
        "description": "Python backend conference",
        "event_type": "CONFERENCE",
        "organizer_id": 1,
        "start_date": "2027-01-20T10:00:00",
        "end_date": "2027-01-20T17:00:00",
        "registration_start": "2026-12-01T10:00:00",
        "registration_end": "2027-01-19T18:00:00",
        "capacity": 100,
        "status": "DRAFT"
    }

    response = client.post(
        "/api/v1/events",
        json=event_data,
        headers=headers,
    )

    assert response.status_code in [200, 201]

    data = response.json()

    assert data["event_name"] == event_data["event_name"]