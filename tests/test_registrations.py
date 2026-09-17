def test_get_registrations(client):

    response = client.get(
        "/api/v1/registrations"
    )

    assert response.status_code == 200


def test_search_registrations(client):

    response = client.get(
        "/api/v1/registrations/search"
    )

    assert response.status_code == 200


def test_get_registration(client):

    response = client.get(
        "/api/v1/registrations/1"
    )

    assert response.status_code in [200, 404]


def test_cancel_registration(client):

    response = client.post(
        "/api/v1/registrations/1/cancel"
    )

    assert response.status_code in [200, 400, 404]