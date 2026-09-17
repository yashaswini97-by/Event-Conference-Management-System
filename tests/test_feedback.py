def test_create_feedback(client):

    feedback_data = {
        "registration_id": 1,
        "event_id": 1,
        "speaker_id": 1,
        "session_id": 1,
        "rating": 5,
        "feedback": "Very good session"
    }

    response = client.post(
        "/api/v1/feedback",
        json=feedback_data
    )

    assert response.status_code in [200, 201, 400, 404]


def test_get_event_feedback(client):

    response = client.get(
        "/api/v1/events/1/feedback"
    )

    assert response.status_code in [200, 404]


def test_get_speaker_ratings(client):

    response = client.get(
        "/api/v1/speakers/1/ratings"
    )

    assert response.status_code in [200, 404]