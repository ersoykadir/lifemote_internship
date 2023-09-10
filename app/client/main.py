"""
Kadir Ersoy
Internship Project
Client for testing the API
"""
import os
import time
import requests
from dotenv import load_dotenv
load_dotenv()

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
API_URL = "http://localhost:3000" # Change to server:3000 when running in docker!
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

def request(req_type, url, headers, payload, params):
    '''Make a request to the server'''
    req = getattr(requests, req_type.lower())
    res = req(url, headers=headers, json=payload, params=params)
    if res.status_code in [400, 401, 403, 404]:
        print(res.status_code, res.json()["detail"])
        raise ValueError(res.status_code, res.json()["detail"])
    if res.status_code == 500:
        print(res.status_code, res.json()["detail"])
        raise ValueError(res.status_code, res.json()["detail"])
    return res.json()

def get_context(context_id):
    '''Get context details'''
    url = f"{API_URL}/contexts/{context_id}"
    context = request("GET", url, HEADERS, None, None)
    print(context)

def get_context_by_name(context_name):
    '''Get context details, given context name'''
    url = f"{API_URL}/contexts"
    params = {"context_name":context_name}
    context = request("GET", url, HEADERS, None, params)
    return context

def get_all_contexts():
    '''Get all contexts'''
    url = f"{API_URL}/contexts/all"
    contexts = request("GET", url, HEADERS, None, None)
    print("Contexts:")
    for context in contexts:
        print("\t", context["name"], context["id"])
    print("------")
    return [c["name"] for c in contexts]

def create_context(name, description):
    '''Create a context'''
    url = f"{API_URL}/contexts/"
    payload = {"name":name, "description":description}
    context = request("POST", url, HEADERS, payload, None)
    print(f"Context with name: '{context['name']}' created")
    print(context)
    return context

def update_context(context_id, name, description):
    '''Update a context'''
    url = f"{API_URL}/contexts/{context_id}"
    payload = {"name":name, "description":description}
    context = request("PUT", url, HEADERS, payload, None)
    print(f"Context with name: '{context['name']}' updated")
    print(context)

def delete_context(context_id):
    '''Delete a context'''
    url = f"{API_URL}/contexts/{context_id}"
    context = request("DELETE", url, HEADERS, None, None)
    print(f"Context with id: '{context['id']}' deleted")
    # print(context)

def get_item(item_id):
    '''Get item details'''
    url = f"{API_URL}/items/{item_id}"
    item = request("GET", url, HEADERS, None, None)
    print(item)

def get_all_items():
    '''Get all items'''
    url = f"{API_URL}/items/all"
    items = request("GET", url, HEADERS, None, None)
    print("Items:")
    for item in items:
        print(f"Item: '{item['message']}, {item['context_id']}'")
    print(f"Items: '{items}'")

def get_context_items(context_name):
    '''Get all items in a context'''
    context = get_context_by_name(context_name)
    print(f"Items in context: '{context['name']}'")
    for item in context["items"]:
        print(f"Item: '{item['message']} {item['id']}'")
    return [item["id"] for item in context["items"]]

def create_item(message, completed, context_name):
    '''Create an item'''
    url = f"{API_URL}/items/"
    payload = {"message":message, "completed":completed, "context_name":context_name}
    item = request("POST", url, HEADERS, payload, None)
    print(f"Item with message: '{item['message']}' created")
    print(item)
    return item

def update_item(item_id, message, completed, context_name):
    '''Update an item'''
    url = f"{API_URL}/items/{item_id}"
    payload = {"message":message, "completed":completed, "context_name":context_name}
    item = request("PUT", url, HEADERS, payload, None)
    print(f"Item with message: '{item['message']}' updated")
    print(item)
    return item

def delete_item(item_id):
    '''Delete an item'''
    url = f"{API_URL}/items/{item_id}"
    item = request("DELETE", url, HEADERS, None, None)
    print(f"Item with id: '{item['id']}' deleted")
    print(item)

def check_connection():
    """Check if server is running"""
    url = f"{API_URL}/"
    try:
        res = request("GET", url, HEADERS, None, None)
        if res["message"] == "Hello World":
            print("Connection successful")
            return True
        print("Connection failed")
        return False
    except ValueError as err:
        print("Connection failed", err)
        return False

def case1():
    """Create context and add items"""

    context_name = "Internship"
    context_description = "Internship tasks"
    item_messages = ["Get Multinet Card", "Refactor Business Logic"]

    context = create_context(context_name, context_description)
    assert context["name"] == context_name

    item1 = create_item(item_messages[0], False, context_name)
    item2 = create_item(item_messages[1], False, context_name)
    items = get_context_items(context_name)
    assert item1["id"] in items and item2["id"] in items

    print("Case 1 passed")

    delete_context(context["id"])

def case2():
    """Add item to a context and update it, then delete item"""

    context = create_context("Internship", "Internship")
    assert context["name"] == "Internship"

    item = create_item("Presentation first draft", False, "Internship")
    updated_item = update_item(item["id"], "Presentation first draft", True, "To-Do")
    # print(item)
    # print(updated_item)
    assert updated_item["context_id"] != item["context_id"]
    delete_item(item["id"])
    items = get_context_items("To-Do")
    assert item["id"] not in items
    print("Case 2 passed")

if __name__ == "__main__":
    print("Trying to connect to server")
    while not check_connection():
        time.sleep(5)

    print(ACCESS_TOKEN)
    all_contexts = get_all_contexts()
    if "Internship" in all_contexts:
        delete_context(get_context_by_name("Internship")["id"])

    case1()

    case2()

    # create context(with no items) and try to delete => WORKS
    # context = create_context("trial1", "trial1")
    # delete_context(context["id"])

    # create context and add items, then try to delete context=> WORKS
    # context1 = create_context("trial2", "trial2")
    # create_item("trial2 item1", False, "trial2")
    # create_item("trial2 item2", False, "trial2")
    # get_context_items("trial2")
    # delete_context(context1["id"])

    # update context => WORKS
    # update_context(8, "Internship", "Internship tasks")
    # update context that you don"t own => WORKS
    # update_context(1, "To-Do", "Internship tasks")
    # update context name to existing context name => Resolved
    # update_context(8, "To-Do", "Internship tasks")

    # get item details => WORKS
    # item = get_item(4)
    # get item details that you don"t own => WORKS
    # item = get_item(9)
    # get context details => WORKS
    # context = get_context(8)
    # get context details that you don"t own => WORKS
    # context = get_context(1)

    # create an item with a context that doesn"t exist => WORKS
    # create_item("trial3 item1", False, "trial3")
    # # create an item with a context that you don"t own => WORKS
    # create_item("trial3 item1", False, "To-Do")

    # update an item => WORKS
    # update_item(10, "trial item updated", True, "Internship")
    # update an item that you don"t own => WORKS
    # update_item(9, "trial3 item1", True, "To-Do")
    # update an item with a context that doesn"t exist => WORKS
    # update_item(10, "trial item updated", True, "To-D")

    # delete an item => WORKS
    # item = create_item("trial item", False, "To-Do")
    # delete_item(item["id"])
    # delete an item that you don"t own => WORKS
    # delete_item(9)

    # delete a context => WORKS
    # context = create_context("Test", "Test")
    # context = get_context_by_name("Test")
    # delete_context(context["id"])

    # delete a context with items => WORKS
    # create_item("Test item", False, "Test")
    # context = get_context_by_name("Test")
    # delete_context(context["id"])

    # delete a context that you don"t own => WORKS
    # delete_context(1)
