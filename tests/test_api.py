import requests, time
from tests.conftest import BASE_URL


# 1. Health / Status endpoint

def test_health_endpoint_returns_healthy():
    response = requests.get(f"{BASE_URL}/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

# 2. User registration

def test_register_user_creates_new_user():
    new_user = f"testuser{int(time.time())}"
    response = requests.post(f"{BASE_URL}/api/auth/register", json={"username": new_user, "password": "testpassword"})
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully"
    assert response.json()["user"]["username"] == new_user
