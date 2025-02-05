from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_chat_endpoint():
    response = client.post(
        "/chat",
        json={"question": "What is AWS Lambda?"}
    )
    assert response.status_code == 200
    assert "response" in response.json()
