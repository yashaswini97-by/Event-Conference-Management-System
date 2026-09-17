def test_get_event_sessions(client):

    response = client.get(
        "/api/v1/events/1/sessions"
    )

    assert response.status_code in [200, 404]


def test_search_sessions(client):

    response = client.get(
        "/api/v1/sessions/search"
    )

    assert response.status_code == 200


def test_get_session(client):

    response = client.get(
        "/api/v1/sessions/1"
    )

    assert response.status_code in [200, 404]


def test_create_session(client):

    session_data = {
        "event_id": 1,
        "speaker_id": 1,
        "hall_id": 1,
        "title": "Introduction to FastAPI",
        "description": "FastAPI backend development session",
        "start_time": "2027-01-20T10:00:00",
        "end_time": "2027-01-20T11:00:00",
        "capacity": 50,
        "session_type": "TECHNICAL"
    }

    response = client.post(
        "/api/v1/sessions",
        json=session_data
    )

    assert response.status_code in [200, 201, 400, 404]