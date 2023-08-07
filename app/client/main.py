import requests, os, time

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