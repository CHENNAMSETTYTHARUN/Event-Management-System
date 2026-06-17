from datetime import datetime, timedelta
from fastapi.testclient import TestClient

def test_registration_flow(client: TestClient, admin_headers, organizer_headers, participant_headers):
    cat_res = client.post(
        "/api/v1/categories",
        json={"name": "Tech Seminar", "description": "Seminars"},
        headers=admin_headers
    )
    cat_id = cat_res.json()["id"]

    future_start = (datetime.now() + timedelta(days=2)).isoformat()
    future_end = (datetime.now() + timedelta(days=3)).isoformat()
    event_res = client.post(
        "/api/v1/events",
        json={
            "name": "Exclusive Seminar",
            "description": "One seat only",
            "category_id": cat_id,
            "start_date": future_start,
            "end_date": future_end,
            "venue": "Meeting Room",
            "capacity": 1,
            "status": "Published"
        },
        headers=organizer_headers
    )
    event_id = event_res.json()["id"]

    reg_res = client.post(
        "/api/v1/registrations",
        json={"event_id": event_id},
        headers=participant_headers
    )
    assert reg_res.status_code == 201
    assert reg_res.json()["status"] == "Confirmed"

    dup_res = client.post(
        "/api/v1/registrations",
        json={"event_id": event_id},
        headers=participant_headers
    )
    assert dup_res.status_code == 409

    client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Second User",
            "email": "second@example.com",
            "password": "password123",
            "role_id": 3
        }
    )
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": "second@example.com", "password": "password123"}
    )
    second_headers = {"Authorization": f"Bearer {login_res.json()['access_token']}"}

    cap_res = client.post(
        "/api/v1/registrations",
        json={"event_id": event_id},
        headers=second_headers
    )
    assert cap_res.status_code == 400
    assert "capacity" in cap_res.json()["error"]["message"].lower()
