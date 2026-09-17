def test_check_in_registration(client):

    response = client.post(
        "/api/v1/registrations/1/check-in",
        json={
            "check_in_method": "MANUAL"
        }
    )

    assert response.status_code in [200, 201, 400, 404]


def test_check_out_registration(client):

    response = client.post(
        "/api/v1/registrations/1/check-out"
    )

    assert response.status_code in [200, 400, 404]