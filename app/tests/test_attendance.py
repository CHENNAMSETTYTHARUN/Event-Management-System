from datetime import datetime, timedelta
from fastapi.testclient import TestClient

def test_attendance_marking_and_summary(client: TestClient, admin_headers, organizer_headers, participant_headers):
    cat_res = client.post(
        "/api/v1/categories",
        json={"name": "Science", "description": "Science events"},
        headers=admin_headers
    )
    cat_id = cat_res.json()["id"]

    future_start = (datetime.now() + timedelta(days=2)).isoformat()
    future_end = (datetime.now() + timedelta(days=3)).isoformat()
    event_res = client.post(
        "/api/v1/events",
        json={
            "name": "Physics Seminar",
            "description": "Physics talk",
            "category_id": cat_id,
            "start_date": future_start,
            "end_date": future_end,
            "venue": "Hall B",
            "capacity": 50,
            "status": "Published"
        },
        headers=organizer_headers
    )
    event_id = event_res.json()["id"]

    prof_res = client.get("/api/v1/auth/profile", headers=participant_headers)
    user_id = prof_res.json()["id"]

    fail_res = client.post(
        "/api/v1/attendance/mark",
        json={
            "event_id": event_id,
            "user_id": user_id,
            "attendance_status": "Present"
        },
        headers=organizer_headers
    )
    assert fail_res.status_code == 400

    client.post(
        "/api/v1/registrations",
        json={"event_id": event_id},
        headers=participant_headers
    )

    succ_res = client.post(
        "/api/v1/attendance/mark",
        json={
            "event_id": event_id,
            "user_id": user_id,
            "attendance_status": "Present"
        },
        headers=organizer_headers
    )
    assert succ_res.status_code == 200
    assert succ_res.json()["attendance_status"] == "Present"

    sum_res = client.get(
        f"/api/v1/attendance/summary/{event_id}",
        headers=organizer_headers
    )
    assert sum_res.status_code == 200
    data = sum_res.json()
    assert data["total_registered"] == 1
    assert data["total_present"] == 1
    assert data["attendance_rate"] == 100.0
