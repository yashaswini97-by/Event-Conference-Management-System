def get_admin_token(client):

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "testadmin@example.com",
            "password": "Admin@12345",
        },
    )

    return response.json()["access_token"]


def test_get_event_tickets(client):

    response = client.get(
        "/api/v1/events/1/tickets"
    )

    assert response.status_code in [200, 404]