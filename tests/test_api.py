from app import app


def test_health_api():

    app.config["TESTING"] = True

    client = app.test_client()

    response = client.get(
        "/api/health"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True