"""
Kadir Ersoy
Internship Project
Test Item Router
"""

import pytest
from fastapi.testclient import TestClient


from server.main import app
from server.routers import extras

from .test_utils import extras_data
from .test_utils.extras_utils import check_response_validity

client = TestClient(app)


@pytest.mark.parametrize(
    "items, property_name, output, status_code",
    extras_data.sort_items_test_data,
)
def test_sort_items(items, property_name, output, status_code):
    """Test sort items"""
    payload = {"items": items, "property_name": property_name}
    response = client.post(
        "/extras/sort_items", json=payload, headers=extras_data.HEADERS
    )
    check_response_validity(response, output, status_code)


@pytest.mark.parametrize(
    "items1, items2, output, status_code",
    extras_data.append_lists_test_data,
)
def test_append_lists(items1, items2, output, status_code):
    """Test append lists"""
    payload = {"items1": items1, "items2": items2}
    response = client.post(
        "/extras/append_lists", json=payload, headers=extras_data.HEADERS
    )
    check_response_validity(response, output, status_code)


@pytest.mark.parametrize(
    "items, complete_status, output, status_code",
    extras_data.filter_list_test_data,
)
def test_filter_list(items, complete_status, output, status_code):
    """Test filter list"""
    payload = {"items": items, "completed": complete_status}
    response = client.post(
        "/extras/filter_list", json=payload, headers=extras_data.HEADERS
    )
    check_response_validity(response, output, status_code)


@pytest.mark.parametrize(
    "override_function, property_name, output, status_code",
    extras_data.sort_itemsv1_test_data,
)
def test_sort_itemsv1(override_function, property_name, output, status_code):
    """Test sort items"""
    payload = {"property_name": property_name, "context_id": 4}
    app.dependency_overrides[extras.get_context_items] = override_function
    response = client.post(
        "/extras/sort_itemsv1", json=payload, headers=extras_data.HEADERS
    )
    check_response_validity(response, output, status_code)
