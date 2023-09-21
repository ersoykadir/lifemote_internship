"""
Kadir Ersoy
Internship Project
Test Main Router
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    """Test root"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
