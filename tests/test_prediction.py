from app import app


def test_prediction_api():

    app.config["TESTING"] = True

    client = app.test_client()

    response = client.post(
        "/api/predict",
        json={
            "area": 1500,
            "bedrooms": 3,
            "bathrooms": 2,
            "floors": 2,
            "location": "Delhi",
            "parking": 1,
            "furnishing": "Furnished",
            "property_type": "Apartment",
            "age": 5
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert "predicted_price" in data