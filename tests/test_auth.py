def test_register_admin(client, admin_user):

    response = client.post(
        "/api/v1/auth/register",
        json=admin_user,
    )

    assert response.status_code in [200, 201]

    data = response.json()

    assert data["email"] == admin_user["email"]


def test_login_admin(client, admin_user):

    # Register first
    client.post(
        "/api/v1/auth/register",
        json=admin_user,
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": admin_user["email"],
            "password": admin_user["password"],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_invalid_login(client):

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "wrong@example.com",
            "password": "WrongPassword",
        },
    )

    assert response.status_code in [401, 404]