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

ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlZXJzb295NjFAZ21haWwuY29tIiwiZXhwIjoxNjkyNjI1NzUyfQ.h5In0Z87O__a5ITQPCWTot6_2ngkzRrzwEyd_o_WzkA'
API_URL = 'http://localhost:3000' # Change to server:3000 when running in docker!
HEADERS = {'Authorization': f'Bearer {ACCESS_TOKEN}'}

def get_contexts():
    url = f'{API_URL}/contexts/'
    contexts = requests.get(url, headers=HEADERS).json()
    print('Contexts:')
    for c in contexts:
        print("\t", c['name'], c['id'])
    print("------")

def create_context(name, description):
    url = f'{API_URL}/contexts/'
    payload = {'name':name, 'description':description}
    context = requests.post(url, json = payload, headers=HEADERS).json()
    print(f'Context with name: "{context["name"]}" created')
    print(context)

def get_context(context_id):
    url = f'{API_URL}/contexts/{context_id}'
    context = requests.get(url, headers=HEADERS).json()
    print(context)

def get_context_items(context_id):
    url = f'{API_URL}/contexts/{context_id}'
    context = requests.get(url, headers=HEADERS).json()
    print(f'Items in context: "{context["name"]}"')
    for item in context['items']:
        print(f'Item: "{item["message"]} {item["id"]}"')

def create_item(message, completed, context_name):
    url = f'{API_URL}/items/'
    payload = {'message':message, 'completed':completed, 'context_name':context_name}
    item = requests.post(url, json = payload, headers=HEADERS).json()
    print(f'Item with message: "{item["message"]}" created')
    print(item)

def get_items():
    url = f'{API_URL}/items/'
    items = requests.get(url, headers=HEADERS).json()
    print('Items:')
    for item in items:
        print(f'Item: "{item["message"]}"')
    print(f'Items: "{items}"')


def update_item(item_id, message, completed, context_name):
    url = f'{API_URL}/items/{item_id}'
    payload = {'message':message, 'completed':completed, 'context_name':context_name}
    item = requests.put(url, json = payload, headers=HEADERS).json()
    print(f'Item with message: "{item["message"]}" updated')
    print(item)

if __name__ == "__main__":
    print('Trying to connect to server')
    while True:
        try:
            # time.sleep(5)
            get_contexts()
            # create_context('test', 'test')
            # create_item('Refactor Client Co', False, 'Internship')
            # get_context_items(42)
            # get_items()
            update_item(62, 'Refactor Client Code', True, 'Internship')
            get_context_items(42)
            break
        except Exception as e:
            print('Error connecting to server')
            print(e)