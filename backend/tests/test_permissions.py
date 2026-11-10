NEW_CASHIER = {
    "name": "New Cashier",
    "email": "new.cashier@example.com",
    "password": "another-password-123",
    "role": "cashier",
}


def test_cashier_can_list_categories(client, auth_headers):
    response = client.get("/api/categories", headers=auth_headers("cashier"))

    assert response.status_code == 200


def test_cashier_cannot_create_users(client, auth_headers):
    response = client.post(
        "/api/users", json=NEW_CASHIER, headers=auth_headers("cashier")
    )

    assert response.status_code == 403


def test_create_user_without_token_returns_401(client):
    response = client.post("/api/users", json=NEW_CASHIER)

    assert response.status_code == 401


def test_owner_can_create_user(client, auth_headers):
    response = client.post(
        "/api/users", json=NEW_CASHIER, headers=auth_headers("owner")
    )

    body = response.get_json()
    assert response.status_code == 201
    assert body["role"] == "cashier"
    assert "password_hash" not in body
