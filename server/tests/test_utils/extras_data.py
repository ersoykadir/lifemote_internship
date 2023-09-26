"""
Kadir Ersoy
Internship Project
Data&Utils for extras route tests
"""
import os
from models.item import Item

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")

HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

ITEMS1 = [
    {
        "message": "Hello World",
        "completed": False,
    },
    {
        "message": "Hello Mars",
        "completed": False,
    },
]

ITEMS2 = [
    {
        "message": "Hello Venus",
        "completed": False,
    },
    {
        "message": "Hello Mercury",
        "completed": False,
    },
]

ITEMS3 = [
    {
        "message": "Hello Jupiter",
        "completed": True,
    },
    {
        "message": "Hello Saturn",
        "completed": False,
    },
    {
        "message": "Hello Uranus",
        "completed": True,
    },
    {
        "message": "Hello Neptune",
        "completed": False,
    },
    {
        "message": "Hello Pluto",
        "completed": True,
    },
]

# Sort items by message
ITEMS1_SORTED = sorted(ITEMS1, key=lambda x: x["message"].lower())

ITEMS2_SORTED = sorted(ITEMS2, key=lambda x: x["message"].lower())

# Filter items by completed
ITEMS3_FILTERED_FALSE = [item for item in ITEMS3 if item["completed"] is False]

ITEMS3_FILTERED_TRUE = [item for item in ITEMS3 if item["completed"] is True]

# Create Item objects from dictionaries
ITEM_OBJECTS1 = [Item(**item) for item in ITEMS1]

ITEM_OBJECTS2 = [Item(**item) for item in ITEMS2]


# Function override for get_context_items
class OverrideGetContextItems:
    """Dependency"""

    def context_items_1(self):
        """Dependency"""
        return ITEM_OBJECTS1

    def context_items_2(self):
        """Dependency"""
        return ITEM_OBJECTS2

    def empty_context_items(self):
        """Dependency"""
        return []

    def nonlist_context_items(self):
        """Dependency"""
        return "Hello World"


OverrideGetContextItems = OverrideGetContextItems()

# Test data for sort_itemsv1
sort_items_test_data = [
    (ITEMS1, "message", ITEMS1_SORTED, 200),
    (ITEMS2, "message", ITEMS2_SORTED, 200),
    ([], "message", [], 200),
    ([3, 2, 1], "message", "Must be a list of dictionaries!", 400),
    ("Hello World", "message", "Input should be a valid list", 422),
]

# Test data for append_lists
append_lists_test_data = [
    ([1, 2, 3], [4, 5, 6], [1, 2, 3, 4, 5, 6], 200),
    (ITEMS1, ITEMS2, ITEMS1 + ITEMS2, 200),
    ([], [], [], 200),
    ("Hello World", "Hello Mars", "Input should be a valid list", 422),
]

# Test data for sort_itemsv1
sort_itemsv1_test_data = [
    (OverrideGetContextItems.context_items_1, "message", ITEMS1_SORTED, 200),
    (OverrideGetContextItems.context_items_2, "message", ITEMS2_SORTED, 200),
    (OverrideGetContextItems.empty_context_items, "message", [], 200),
    (
        OverrideGetContextItems.nonlist_context_items,
        "message",
        "Input should be a valid list",
        400,
    ),
]

# Test data for filter_list
filter_list_test_data = [
    (ITEMS3, "completed", False, ITEMS3_FILTERED_FALSE, 200),
    (ITEMS3, "completed", True, ITEMS3_FILTERED_TRUE, 200),
    ([], False, [], 200),
    ([], True, [], 200),
    ("Hello World", False, "Input should be a valid list", 422),
]
