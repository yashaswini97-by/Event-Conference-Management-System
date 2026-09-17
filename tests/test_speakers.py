def test_get_speakers(client):

    response = client.get(
        "/api/v1/speakers"
    )

    assert response.status_code == 200


def test_get_speaker(client):

    response = client.get(
        "/api/v1/speakers/1"
    )

    assert response.status_code in [200, 404]


def test_create_speaker(client):

    speaker_data = {
        "name": "Rahul Sharma",
        "email": "rahul.speaker@example.com",
        "phone": "9876543210",
        "bio": "Experienced technology speaker",
        "expertise": "Python and FastAPI",
        "company": "Tech Solutions",
        "experience": 8
    }

    response = client.post(
        "/api/v1/speakers",
        json=speaker_data
    )

    assert response.status_code in [200, 201, 400]


def test_update_speaker(client):

    speaker_data = {
        "name": "Rahul Sharma Updated",
        "bio": "Senior Python developer and speaker"
    }

    response = client.put(
        "/api/v1/speakers/1",
        json=speaker_data
    )

    assert response.status_code in [200, 400, 404]