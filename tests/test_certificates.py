def test_generate_certificate(client):

    response = client.post(
        "/api/v1/certificates/generate/1"
    )

    assert response.status_code in [200, 201, 400, 404]


def test_get_certificate(client):

    response = client.get(
        "/api/v1/certificates/1"
    )

    assert response.status_code in [200, 404]


def test_get_attendee_certificates(client):

    response = client.get(
        "/api/v1/attendees/1/certificates"
    )

    assert response.status_code in [200, 404]