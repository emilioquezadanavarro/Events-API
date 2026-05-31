import requests, time
from tests.conftest import BASE_URL

# **************** Core Integration Tests (Happy Path) ************************

# 1. Health / Status endpoint

def test_health_endpoint_returns_healthy():
    response = requests.get(f"{BASE_URL}/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

# 2. User registration

def test_register_user_creates_new_user():
    new_user = f"testuser{int(time.time_ns())}"
    response = requests.post(f"{BASE_URL}/api/auth/register", json={"username": new_user, "password": "testpassword"})
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully"
    assert response.json()["user"]["username"] == new_user

# 3. User login

def test_test_login_returns_jwt_token():
    user_test = requests.post(f"{BASE_URL}/api/auth/register", json={"username": f"testuser_two{int(time.time_ns())}", "password": "testpassword"})
    print(user_test.json())
    response = requests.post(f"{BASE_URL}/api/auth/login", json={"username": user_test.json()["user"]["username"], "password": "testpassword"})
    assert response.status_code == 200
    assert response.json()["access_token"] is not None

#4. Create event (authenticated)

def test_create_public_event_requires_auth_and_succeeds_with_token():
    # Register a new user
    user_test = requests.post(f"{BASE_URL}/api/auth/register", json={"username": f"testuser_three{int(time.time_ns())}", "password": "testpassword"})

    # Login the new user
    login_user_test = requests.post(f"{BASE_URL}/api/auth/login", json={"username": user_test.json()["user"]["username"], "password": "testpassword"})

    # Getting the Access token
    access_token = login_user_test.json()["access_token"]

    # Create Event
    response = requests.post(f"{BASE_URL}/api/events", json={"title": "Test Event", "date": "2026-07-19", "is_public": True,}, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test Event"
    assert response.json()["date"] == "2026-07-19T00:00:00"

# 5. RSVP to a public event

def test_rsvp_to_public_event_succeeds_without_auth():
    # Register a new user
    user_test = requests.post(f"{BASE_URL}/api/auth/register", json={"username": f"testuser_four{int(time.time_ns())}", "password": "testpassword"})

    # Login the new user
    login_user_test = requests.post(f"{BASE_URL}/api/auth/login", json={"username": user_test.json()["user"]["username"], "password": "testpassword"})

    # Getting the Access token
    access_token = login_user_test.json()["access_token"]

    # Create Event
    event = requests.post(f"{BASE_URL}/api/events",
                             json={"title": "Test Event", "date": "2026-07-19", "is_public": True, },
                             headers={"Authorization": f"Bearer {access_token}"})

    # Getting the Event id
    event_id = event.json()["id"]

    # RSVP to the event
    response = requests.post(f"{BASE_URL}/api/rsvps/event/{event_id}", json={"attending": True})
    assert response.status_code == 201
    assert response.json()["event_id"] == event_id

# **************** Error / Edge‑Case Tests ************************

# 1. Duplicate username registration

def test_duplicate_username_registration():

    new_user = f"testuser_five{int(time.time_ns())}"
    response = requests.post(f"{BASE_URL}/api/auth/register", json={"username": new_user, "password": "testpassword"})
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully"
    assert response.json()["user"]["username"] == new_user

    response = requests.post(f"{BASE_URL}/api/auth/register", json={"username": new_user, "password": "testpassword"})
    assert response.status_code == 400
    assert response.json()["error"] == "Username already exists"

# 2. Create event without auth

def test_create_event_without_auth():

    # Create Event
    response = requests.post(f"{BASE_URL}/api/events", json={"title": "Test Event", "date": "2026-07-19", "is_public": True, })
    assert response.status_code == 401
    assert response.json()["msg"] == "Missing Authorization Header"

# 3. RSVP to non‑public event without auth

def test_rsvp_to_non_public_event_without_auth():

    # Register a new user
    user_test = requests.post(f"{BASE_URL}/api/auth/register", json={"username": f"testuser_six{int(time.time_ns())}", "password": "testpassword"})

    # Login the new user
    login_user_test = requests.post(f"{BASE_URL}/api/auth/login", json={"username": user_test.json()["user"]["username"], "password": "testpassword"})

    # Getting the Access token
    access_token = login_user_test.json()["access_token"]

    # Create Event
    event = requests.post(f"{BASE_URL}/api/events",
                             json={"title": "Test Event", "date": "2026-07-19", "is_public": False, }, headers={"Authorization": f"Bearer {access_token}"})

    # Getting the Event id
    event_id = event.json()["id"]

    # RSVP to the event without token
    response = requests.post(f"{BASE_URL}/api/rsvps/event/{event_id}", json={"attending": True})
    assert response.status_code == 401
    assert response.json()["error"] == "Authentication required for this event"

