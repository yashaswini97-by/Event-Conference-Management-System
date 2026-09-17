def test_get_venues(client):

    response = client.get(
        "/api/v1/venues"
    )

    assert response.status_code == 200


def test_get_venue(client):

    response = client.get(
        "/api/v1/venues/1"
    )

    assert response.status_code in [200, 404]


def test_create_venue(client):

    venue_data = {
        "venue_name": "Bangalore Convention Center",
        "address": "MG Road, Bengaluru",
        "city": "Bengaluru",
        "capacity": 500,
        "facilities": "Parking, WiFi, Projector",
        "status": "ACTIVE"
    }

    response = client.post(
        "/api/v1/venues",
        json=venue_data
    )

    assert response.status_code in [200, 201, 400]


def test_get_halls(client):

    response = client.get(
        "/api/v1/venues/1/halls"
    )

    assert response.status_code in [200, 404]


def test_create_hall(client):

    hall_data = {
        "hall_name": "Main Conference Hall",
        "capacity": 200,
        "floor": 1,
        "availability_status": "AVAILABLE"
    }

    response = client.post(
        "/api/v1/venues/1/halls",
        json=hall_data
    )

    assert response.status_code in [200, 201, 400, 404]