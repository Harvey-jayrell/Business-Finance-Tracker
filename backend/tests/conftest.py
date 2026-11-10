import pytest
from app import create_app
from app.extensions import db, bcrypt
from app.models.user import User

TEST_PASSWORD = "test-password-123"
TEST_JWT_SECRET = "test-secret-key-that-is-at-least-32-bytes-long"

@pytest.fixture
def app(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", TEST_JWT_SECRET)
    app = create_app("testing")

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def make_user(app):
    def _make_user(role, email, password=TEST_PASSWORD):
        with app.app_context():
            hashed = bcrypt.generate_password_hash(password).decode("utf-8")
            db.session.add(
                User(name=f"Test {role}", email=email, password_hash=hashed, role=role)
            )
            db.session.commit()

    return _make_user


@pytest.fixture
def auth_headers(client, make_user):
    def _auth_headers(role):
        email = f"{role}@example.com"
        make_user(role, email)
        response = client.post(
            "/api/auth/login", json={"email": email, "password": TEST_PASSWORD}
        )
        token = response.get_json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    return _auth_headers
