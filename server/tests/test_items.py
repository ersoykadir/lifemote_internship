"""
Kadir Ersoy
Internship Project
Test Item Router
"""
import os
from fastapi.testclient import TestClient

from server.main import app

client = TestClient(app)

TEST_ITEM = None
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
print(ACCESS_TOKEN)
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# The following tests are commented out
# because they require a database running.
# They can be used later on for integration testing,
# with not only single requests but a set of requests for a specific use case.

# def test_create_item():
#     """ Test create item"""
#     payload = {
#         "message": "Hello World",
#         "completed": False,
#         "context_name": "To-Do"
#     }
#     response = client.post("/items/", json=payload, headers=HEADERS)
#     print(response.json())
#     assert response.status_code == 201
#     assert response.json()["message"] == payload["message"]
#     assert response.json()["completed"] == payload["completed"]

#     global TEST_ITEM
#     TEST_ITEM = response.json()


# def test_get_item():
#     """ Test get item"""
#     response = client.get(f"/items/{TEST_ITEM['id']}", headers=HEADERS)
#     assert response.status_code == 200
#     assert response.json() == TEST_ITEM

# def test_get_items():
#     """ Test get items"""
#     response = client.get("/items/all", headers=HEADERS)
#     assert response.status_code == 200
#     assert len(response.json()) > 0

# def test_update_item():
#     """ Test update item"""
#     payload = {
#         "message": "Hello Mars",
#         "completed": False,
#         "context_name": "To-Do"
#     }
#     response = client.put(
#         f"/items/{TEST_ITEM['id']}", json=payload, headers=HEADERS
#     )
#     assert response.status_code == 200
#     assert response.json()["message"] == payload["message"]
#     assert response.json()["id"] == TEST_ITEM["id"]

# def test_delete_item():
#     """ Test delete item"""
#     response = client.delete(f"/items/{TEST_ITEM['id']}", headers=HEADERS)
#     assert response.status_code == 200
#     assert response.json()["message"] == "Hello Mars"
#     assert response.json()["id"] == TEST_ITEM["id"]
