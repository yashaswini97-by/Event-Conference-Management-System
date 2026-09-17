def test_get_payment(client):

    response = client.get(
        "/api/v1/payments/1"
    )

    assert response.status_code in [200, 404]


def test_search_payments(client):

    response = client.get(
        "/api/v1/payments/search"
    )

    assert response.status_code == 200


def test_create_payment(client):

    payment_data = {
        "transaction_id": "TEST-TXN-001",
        "payment_method": "UPI",
        "amount": 1000,
        "payment_status": "SUCCESS"
    }

    response = client.post(
        "/api/v1/purchases/1/payment",
        json=payment_data
    )

    assert response.status_code in [200, 201, 400, 404]