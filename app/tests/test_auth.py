from fastapi.testclient import TestClient

def test_register_user(client: TestClient):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "New User",
            "email": "newuser@example.com",
            "phone": "+12028889999",
            "password": "password123",
            "role_id": 3
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["full_name"] == "New User"
    assert "password" not in data

def test_login_user(client: TestClient):
    client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Login User",
            "email": "loginuser@example.com",
            "phone": "+12028889988",
            "password": "password123",
            "role_id": 3
        }
    )

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "loginuser@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

def test_get_profile(client: TestClient, participant_headers):
    response = client.get("/api/v1/auth/profile", headers=participant_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testparticipant@example.com"
