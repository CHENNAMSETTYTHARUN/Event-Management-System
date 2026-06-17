from datetime import datetime, timedelta
from fastapi.testclient import TestClient

def test_ticket_generation_and_validation(client: TestClient, admin_headers, organizer_headers, participant_headers):
    cat_res = client.post(
        "/api/v1/categories",
        json={"name": "Gaming", "description": "Gaming events"},
        headers=admin_headers
    )
    cat_id = cat_res.json()["id"]

    future_start = (datetime.now() + timedelta(days=2)).isoformat()
    future_end = (datetime.now() + timedelta(days=3)).isoformat()
    event_res = client.post(
        "/api/v1/events",
        json={
            "name": "E-Sports Tournament",
            "description": "Gaming tournament",
            "category_id": cat_id,
            "start_date": future_start,
            "end_date": future_end,
            "venue": "Cyber Cafe",
            "capacity": 20,
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
    reg_id = reg_res.json()["id"]

    ticket_res = client.post(
        "/api/v1/tickets/generate",
        json={"registration_id": reg_id},
        headers=participant_headers
    )
    assert ticket_res.status_code == 201
    ticket_data = ticket_res.json()
    assert "ticket_number" in ticket_data
    assert "qr_code" in ticket_data
    assert ticket_data["status"] == "Active"

    val_res = client.post(
        "/api/v1/tickets/validate",
        json={
            "ticket_number": ticket_data["ticket_number"],
            "event_id": event_id
        },
        headers=organizer_headers
    )
    assert val_res.status_code == 200
    assert val_res.json()["valid"] is True
