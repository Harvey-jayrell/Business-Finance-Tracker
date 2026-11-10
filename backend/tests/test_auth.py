def test_login_wrong_password_returns_401(client, make_user):
    make_user("owner", "owner@example.com", "right-password")

    response = client.post(
        "/api/auth/login",
        json={"email": "owner@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.get_json() == {"error": "Invalid Credentials"}

def test_login_success_returns_token(client, make_user):
    make_user("owner", "owner@example.com", "right-password")

    response = client.post(
        "/api/auth/login",
        json={"email": "owner@example.com", "password": "right-password"},
    )

    body = response.get_json()
    assert response.status_code == 200
    assert body["access_token"]
    assert body["role"] == "owner"
    assert "password_hash" not in body
