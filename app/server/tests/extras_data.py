"""
Kadir Ersoy
Internship Project
Data for extras tests
"""
import os
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
HEADERS = {
    "Authorization": "Bearer {ACCESS_TOKEN}"
}
ITEMS1 = [
    {
        "message": "Hello World",
        "completed": False,
    },
    {
        "message": "Hello Mars",
        "completed": False,
    }
]
ITEMS2 = [
    {
        "message": "Hello Venus",
        "completed": False,
    },
    {
        "message": "Hello Mercury",
        "completed": False,
    }
]
ITEMS1_SORTED = [
    {
        "message": "Hello Mars",
        "completed": False,
    },
    {
        "message": "Hello World",
        "completed": False,
    }
]
ITEMS2_SORTED = [
    {
        "message": "Hello Mercury",
        "completed": False,
    },
    {
        "message": "Hello Venus",
        "completed": False,
    }
]
from models.item import Item
_ITEMS1 = [ Item(**item) for item in ITEMS1 ]
_ITEMS2 = [ Item(**item) for item in ITEMS2 ]
_ITEMS1_SORTED = [ Item(**item) for item in ITEMS1_SORTED ]
_ITEMS2_SORTED = [ Item(**item) for item in ITEMS2_SORTED ]
