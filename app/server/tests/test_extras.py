"""
Kadir Ersoy
Internship Project
Test Item Router
"""
import sys
import os
from dotenv import load_dotenv
from fastapi.testclient import TestClient

# Add the top-level directory (backend) to sys.path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, backend_path)

from main import app
from routers import extras
import extras_data

load_dotenv()
client = TestClient(app)


def override_get_context_items():
    """Dependency"""
    return extras_data._ITEMS1

def override_get_context_items_empty():
    """Dependency"""
    return []

def override_get_context_items_nonlist():
    """Dependency"""
    return "Hello World"

def test_sort_items():
    """ Test sort items"""
    payload = {
        "items": extras_data.ITEMS1,
        "property_name": "message"
    }
    response = client.post("/extras/sort_items", json=payload, headers=extras_data.HEADERS)
    assert response.status_code == 200
    assert response.json() == extras_data.ITEMS1_SORTED

def test_append_lists():
    """ Test append lists"""
    payload = {
        "items1": extras_data.ITEMS1,
        "items2": extras_data.ITEMS2
    }
    response = client.post("/extras/append_lists", json=payload, headers=extras_data.HEADERS)
    assert response.status_code == 200
    assert response.json() == extras_data.ITEMS1 + extras_data.ITEMS2

def test_filter_list():
    """ Test filter list"""
    payload = {
        "items": [
            {
                "message": "Hello World",
                "completed": False,
            },
            {
                "message": "Hello Mars",
                "completed": True,
            }
        ],
        "completed": False
    }
    response = client.post("/extras/filter_list", json=payload, headers=extras_data.HEADERS)
    assert response.status_code == 200
    assert response.json() == [
        {
            "message": "Hello World",
            "completed": False,
        }
    ]

def test_sort_itemsv1():
    """ Test sort items"""
    payload = {
        "property_name": "message",
        "context_id" : 4
    }
    app.dependency_overrides[extras.get_context_items] = override_get_context_items
    response = client.post("/extras/sort_itemsv1", json=payload, headers=extras_data.HEADERS)
    assert response.status_code == 200
    assert response.json() == extras_data.ITEMS1_SORTED

def test_sort_itemsv1_emptylist():
    """ Test sort items"""
    payload = {
        "property_name": "message",
        "context_id" : 4
    }
    app.dependency_overrides[extras.get_context_items] = override_get_context_items_empty
    response = client.post("/extras/sort_itemsv1", json=payload, headers=extras_data.HEADERS)
    assert response.status_code == 200
    assert response.json() == []

def test_sort_itemsv1_nonlist():
    """ Test sort items"""
    payload = {
        "property_name": "message",
        "context_id" : 4
    }
    app.dependency_overrides[extras.get_context_items] = override_get_context_items_nonlist
    response = client.post("/extras/sort_itemsv1", json=payload, headers=extras_data.HEADERS)
    assert response.status_code == 400
    assert response.json().get("detail") == "Must be a list of dictionaries!"
