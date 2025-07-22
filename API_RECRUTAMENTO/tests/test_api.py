# tests/test_api.py

from fastapi.testclient import TestClient
from api.app import app  # ajuste se necessário

client = TestClient(app)

def test_predict_endpoint():
    response = client.post("/predict", json={"feature1": 1.5, "feature2": 0.8, "feature3": "valor"})
    assert response.status_code == 200
    assert "contratado_predito" in response.json()
