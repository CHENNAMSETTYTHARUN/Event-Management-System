from datetime import datetime, timedelta
from fastapi.testclient import TestClient

def test_create_and_list_event(client: TestClient, admin_headers, organizer_headers):
    cat_res = client.post(
        "/api/v1/categories",
        json={"name": "Conference", "description": "Conferences"},
        headers=admin_headers
    )
    cat_id = cat_res.json()["id"]

    future_start = (datetime.now() + timedelta(days=2)).isoformat()
    future_end = (datetime.now() + timedelta(days=3)).isoformat()

    response = client.post(
        "/api/v1/events",
        json={
            "name": "Python Conference 2026",
            "description": "Python community conference",
            "category_id": cat_id,
            "start_date": future_start,
            "end_date": future_end,
            "venue": "Convention Center",
            "capacity": 100,
            "status": "Published"
        },
        headers=organizer_headers
    )
    assert response.status_code == 201
    event_data = response.json()
    assert event_data["name"] == "Python Conference 2026"
    assert event_data["capacity"] == 100

    list_res = client.get("/api/v1/events")
    assert list_res.status_code == 200
    assert list_res.json()["total"] >= 1
