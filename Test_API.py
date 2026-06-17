from fastapi.testclient import TestClient

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_single_predict():
    payload = {
        "customer_id": "TEST001",
        "features": {
            "recency_days": 15,
            "monetary_180d": 2500.50,
            "ticket_count_90d": 0
        }
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "churn_probability" in data
    assert "risk_level" in data
    assert data["customer_id"] == "TEST001"

def test_batch_predict():
    payload = {
        "customers": [
            {"customer_id": "TEST001", "features": {"recency_days": 15}},
            {"customer_id": "TEST002", "features": {"recency_days": 120}}
        ]
    }
    response = client.post("/batch_predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["predictions"]) == 2
    assert data["predictions"][0]["customer_id"] == "TEST001"
