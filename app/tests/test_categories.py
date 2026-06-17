from fastapi.testclient import TestClient

def test_admin_create_category(client: TestClient, admin_headers):
    response = client.post(
        "/api/v1/categories",
        json={"name": "Testing Category", "description": "Category for unit tests"},
        headers=admin_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Testing Category"

def test_organizer_cannot_create_category(client: TestClient, organizer_headers):
    response = client.post(
        "/api/v1/categories",
        json={"name": "Should Fail", "description": "Organizer not allowed"},
        headers=organizer_headers
    )
    assert response.status_code == 403
