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

load_dotenv()
client = TestClient(app)

# For now, I will use the real database for testing
# TODO: Try to mock the database

TOKEN = os.environ.get("ACCESS_TOKEN")
print(TOKEN)
HEADERS = {
    "Authorization": "Bearer {TOKEN}"
}

def test_sort_items():
    """ Test sort items"""
    payload = {
        "items": [
            {
                "message": "Hello World",
                "completed": False,
                "context_name": "To-Do"
            },
            {
                "message": "Hello Mars",
                "completed": False,
                "context_name": "To-Do"
            }
        ],
        "property_name": "message"
    }
    response = client.post("/extras/sort_items", json=payload, headers=HEADERS)
    assert response.status_code == 200
    assert response.json() == [
        {
            "message": "Hello Mars",
            "completed": False,
            "context_name": "To-Do"
        },
        {
            "message": "Hello World",
            "completed": False,
            "context_name": "To-Do"
        }
    ]

def test_append_lists():
    """ Test append lists"""
    payload = {
        "items1": [
            {
                "message": "Hello World",
                "completed": False,
                "context_name": "To-Do"
            },
            {
                "message": "Hello Mars",
                "completed": False,
                "context_name": "To-Do"
            }
        ],
        "items2": [
            {
                "message": "Hello Venus",
                "completed": False,
                "context_name": "To-Do"
            },
            {
                "message": "Hello Mercury",
                "completed": False,
                "context_name": "To-Do"
            }
        ]
    }
    response = client.post("/extras/append_lists", json=payload, headers=HEADERS)
    assert response.status_code == 200
    assert response.json() == [
        {
            "message": "Hello World",
            "completed": False,
            "context_name": "To-Do"
        },
        {
            "message": "Hello Mars",
            "completed": False,
            "context_name": "To-Do"
        },
        {
            "message": "Hello Venus",
            "completed": False,
            "context_name": "To-Do"
        },
        {
            "message": "Hello Mercury",
            "completed": False,
            "context_name": "To-Do"
        }
    ]

def test_filter_list():
    """ Test filter list"""
    payload = {
        "items": [
            {
                "message": "Hello World",
                "completed": False,
                "context_name": "To-Do"
            },
            {
                "message": "Hello Mars",
                "completed": True,
                "context_name": "To-Do"
            }
        ],
        "completed": False
    }
    response = client.post("/extras/filter_list", json=payload, headers=HEADERS)
    assert response.status_code == 200
    assert response.json() == [
        {
            "message": "Hello World",
            "completed": False,
            "context_name": "To-Do"
        }
    ]
