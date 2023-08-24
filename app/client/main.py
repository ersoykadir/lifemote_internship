import requests, os, time

# Flow
# 1. Client registers with their google account
# 1.1 Client gets redirected to google
# 1.2 Client gets an access token
# 1.3. Client sends request to server with access token
# 2. Client checks their contexts
# 3. Client creates a context
# 4. Client creates an item
# 5. Client checks their items
# 6. Client updates an item

ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlZXJzb295NjFAZ21haWwuY29tIiwiZXhwIjoxNjkyODg3NzkzfQ.1ToBWFSfn5yobDdnn4AfZAqXp23hOMX-ik3o2T7kioY'
API_URL = 'http://localhost:3000' # Change to server:3000 when running in docker!
HEADERS = {'Authorization': f'Bearer {ACCESS_TOKEN}'}

def request(type, url, headers, payload, params):
    if type == 'GET':
        res = requests.get(url, headers=headers, json=payload, params=params)
    elif type == 'POST':
        res = requests.post(url, headers=headers, json=payload, params=params)
    elif type == 'PUT':
        res = requests.put(url, headers=headers, json=payload, params=params)
    elif type == 'DELETE':
        res = requests.delete(url, headers=headers, json=payload, params=params)
    else:
        raise Exception('Invalid request type')
    # print(res.status_code, res.json())
    if res.status_code == 400 or res.status_code == 401 or res.status_code == 404:
        print(res.status_code, res.json()['detail'])
        return None
    if res.status_code == 500:
        raise Exception('Server error')
    return res.json()

def get_context(context_id):
    url = f'{API_URL}/contexts/{context_id}'
    context = requests.get(url, headers=HEADERS).json()
    print(context)

def get_context_by_name(context_name):
    url = f'{API_URL}/contexts'
    params = {'context_name':context_name}
    context = request('GET', url, HEADERS, None, params)
    return context

def get_all_contexts():
    url = f'{API_URL}/contexts/all'
    contexts = request('GET', url, HEADERS, None, None)
    if contexts == None:
        return
    print('Contexts:')
    for c in contexts:
        print("\t", c['name'], c['id'])
    print("------")

def create_context(name, description):
    url = f'{API_URL}/contexts/'
    payload = {'name':name, 'description':description}
    context = request('POST', url, HEADERS, payload, None)
    if context == None:
        return
    print(f'Context with name: "{context["name"]}" created')
    print(context)
    return context

def update_context(context_id, name, description):
    url = f'{API_URL}/contexts/{context_id}'
    payload = {'name':name, 'description':description}
    context = request('PUT', url, HEADERS, payload, None)
    if context == None:
        return
    print(f'Context with name: "{context["name"]}" updated')
    print(context)

def delete_context(context_id):
    url = f'{API_URL}/contexts/{context_id}'
    context = request('DELETE', url, HEADERS, None, None)
    if context == None:
        return
    print(f'Context with id: "{context["id"]}" deleted')
    print(context)

def get_item(item_id):
    url = f'{API_URL}/items/{item_id}'
    item = requests.get(url, headers=HEADERS).json()
    print(item)

def get_all_items():
    url = f'{API_URL}/items/all'
    items = request('GET', url, HEADERS, None, None)
    print('Items:')
    for item in items:
        print(f'Item: "{item["message"]}, {item["context_id"]}"')
    print(f'Items: "{items}"')

def get_context_items(context_name):
    context = get_context_by_name(context_name)
    if context == None:
        return
    print(f'Items in context: "{context["name"]}"')
    for item in context['items']:
        print(f'Item: "{item["message"]} {item["id"]}"')

def create_item(message, completed, context_name):
    url = f'{API_URL}/items/'
    payload = {'message':message, 'completed':completed, 'context_name':context_name}
    item = request('POST', url, HEADERS, payload, None)
    print(f'Item with message: "{item["message"]}" created')
    print(item)

def update_item(item_id, message, completed, context_name):
    url = f'{API_URL}/items/{item_id}'
    payload = {'message':message, 'completed':completed, 'context_name':context_name}
    item = request('PUT', url, HEADERS, payload, None)
    print(f'Item with message: "{item["message"]}" updated')
    print(item)

def delete_item(item_id):
    url = f'{API_URL}/items/{item_id}'
    item = request('DELETE', url, HEADERS, None, None)
    if item == None:
        return
    print(f'Item with id: "{item["id"]}" deleted')
    print(item)

def check_connection():
    url = f'{API_URL}/'
    res = request('GET', url, HEADERS, None, None)
    if res['message'] == 'Hello World':
        print('Connection successful')
        return True
    else:
        print('Connection failed')
        return False

if __name__ == "__main__":
    print('Trying to connect to server')
    while not check_connection():
        time.sleep(5)

    get_all_contexts()
    create_context('Internship', 'Internship')
    context = get_context_by_name('Internship')
    # create_item('Refactor Business Logic', False, 'Internship')
    get_context_items('Internship')
    # create_item('Presentation first draft', False, 'Internship')
    # update_item(64, 'Presentation first draft', True, 'To-Do')
    get_context_items('To-Do')
    delete_item(65)
    get_context_items('To-Do')

    # create context and try to delete => WORKS
    # context = create_context('trial1', 'trial1')
    # delete_context(context['id'])

    # create context and add items, then try to delete => FAILS
    # context = create_context('trial2', 'trial2')
    # create_item('trial2 item1', False, 'trial2')
    # create_item('trial2 item2', False, 'trial2')
    delete_context(context['id'])
