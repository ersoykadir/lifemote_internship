"""
Kadir Ersoy
Internship Project
Test Item Router
"""
import sys
import os
import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

# Add the top-level directory (backend) to sys.path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, backend_path)

from main import app
from routers import extras
from tests.utils import extras as extras_utils
from tests.utils.utils import check_response_validity

load_dotenv()
client = TestClient(app)

@pytest.mark.parametrize("items, property_name, output, status_code", extras_utils.sort_items_test_data)
def test_sort_items(items, property_name, output, status_code):
    """ Test sort items"""
    payload = {
        "items": items,
        "property_name": property_name
    }
    response = client.post("/extras/sort_items", json=payload, headers=extras_utils.HEADERS)
    check_response_validity(response, output, status_code)

@pytest.mark.parametrize("items1, items2, output, status_code", extras_utils.append_lists_test_data)
def test_append_lists(items1, items2, output, status_code):
    """ Test append lists"""
    payload = {
        "items1": items1,
        "items2": items2
    }
    response = client.post("/extras/append_lists", json=payload, headers=extras_utils.HEADERS)
    check_response_validity(response, output, status_code)

@pytest.mark.parametrize("items, complete_status, output, status_code", extras_utils.filter_list_test_data)
def test_filter_list(items, complete_status, output, status_code):
    """ Test filter list"""
    payload = {
        "items": items,
        "completed": complete_status
    }
    response = client.post("/extras/filter_list", json=payload, headers=extras_utils.HEADERS)
    check_response_validity(response, output, status_code)

@pytest.mark.parametrize("override_function, property_name, output, status_code", extras_utils.sort_itemsv1_test_data)
def test_sort_itemsv1(override_function, property_name, output, status_code):
    """ Test sort items"""
    payload = {
        "property_name": property_name,
        "context_id" : 4
    }
    app.dependency_overrides[extras.get_context_items] = override_function
    response = client.post("/extras/sort_itemsv1", json=payload, headers=extras_utils.HEADERS)
    check_response_validity(response, output, status_code)
