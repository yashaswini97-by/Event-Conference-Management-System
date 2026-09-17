def get_admin_token(client):

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "testadmin@example.com",
            "password": "Admin@12345",
        },
    )

    return response.json()["access_token"]


def test_admin_dashboard(client):

    token = get_admin_token(client)

    response = client.get(
        "/api/v1/analytics/admin/dashboard",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "total_events" in data
    assert "total_attendees" in data
    assert "total_registrations" in data
    assert "tickets_sold" in data
    assert "revenue" in data


def test_admin_reports(client):

    token = get_admin_token(client)

    response = client.get(
        "/api/v1/analytics/admin/reports",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "daily_registrations" in data
    assert "event_revenue" in data
    assert "ticket_sales" in data
    assert "attendance" in data
    assert "speaker_ratings" in data
    assert "session_popularity" in data