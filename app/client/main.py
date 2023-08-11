import requests, os, time

# Flow
# 1. Client creates a user
# 2. Client checks their contexts
# 3. Client creates a context
# 4. Client creates an item
# 5. Client checks their items
# 6. Client updates an item

def create_user():
    print('Creating user')
    user = requests.post(f'http://server:3000/users/', json = {'email':'test', 'password':'test'})
    print(f'User with email: "{user.email}" created')

def get_contexts(user_id):
    contexts = requests.get(f'http://server:3000/users/{user_id}/contexts/')
    print(f'User with id: "{user_id}" has contexts: "{contexts}"')

def create_context(user_id, name, description):
    context = requests.post(f'http://server:3000/users/{user_id}/contexts/', json = {'name':name, 'description':description})
    print(f'Context with name: "{context.name}" created')

def create_item(user_id, message, completed, context_name):
    item = requests.post(f'http://server:3000/users/{user_id}/items/', json = {'message':message, 'completed':completed, 'context_name':context_name})
    print(f'Item with message: "{item.message}" created')
    print(item)

def get_items():
    items = requests.get(f'http://server:3000/items/')
    print(f'Items: "{items}"')

def update_item(user_id, message, completed, context_name):
    item = requests.put(f'http://server:3000/items/', json = {'message':message, 'completed':completed, 'context_name':context_name})
    print(f'Item with message: "{item.message}" updated')
    print(item)

if __name__ == "__main__":
    print('Trying to connect to server')
    while True:
        try:
            time.sleep(5)
            # Static IP
            # x = requests.get(f'http://server:{os.environ.get("SERVER_PORT")}/items/1')
            y = requests.post(f'http://server:3000/items/', json = {'message':'test'})
            print(y.text)
            break
        except Exception as e:
            print('Error connecting to server')
            print(e)