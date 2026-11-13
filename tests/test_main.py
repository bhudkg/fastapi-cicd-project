from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["version"] == "1.0.0"


def test_health():
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json()["status"] == "alive"


def test_database_readiness():
    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"
    assert response.json()["database"] == "connected"


def test_create_item():
    response = client.post(
        "/items/",
        json={
            "name": "MacBook Air",
            "description": "Development laptop",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "MacBook Air"
    assert data["description"] == "Development laptop"
    assert "id" in data


def test_get_items():
    response = client.get("/items/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_item_not_found():
    response = client.get("/items/999999")

    assert response.status_code == 404


def test_update_item():
    create_response = client.post(
        "/items/",
        json={"name": "Keyboard"},
    )

    item_id = create_response.json()["id"]

    response = client.patch(
        f"/items/{item_id}",
        json={"name": "Mechanical Keyboard"},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Mechanical Keyboard"


def test_delete_item():
    create_response = client.post(
        "/items/",
        json={"name": "Temporary Item"},
    )

    item_id = create_response.json()["id"]

    response = client.delete(f"/items/{item_id}")

    assert response.status_code == 204

    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404
