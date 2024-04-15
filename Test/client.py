import sys
import threading
import time
from datetime import datetime
import socketio

# Create a SocketIO instance
sio = socketio.Client()

# Define functions to handle events
@sio.on('message')
def handle_message(message):
    print('\n', message)

def connect_to_server(host_address, port_number):
    try:
        sio.connect('http://' + host_address + ':' + str(port_number))
        print("\nConnected to the server.\n")
    except Exception as e:
        print("\nError connecting to the server:", e)
        sys.exit()

def send_client_message():
    while True:
        user_input = input()
        sio.send(user_input)

def main():
    try:
        default_host = "127.0.0.1"
        default_port = 5000

        connect_to_server(default_host, default_port)

        response_thread = threading.Thread(target=send_client_message)
        response_thread.daemon = True
        response_thread.start()

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sio.disconnect()
        print("\nDisconnected from the server.\n")
        sys.exit()

main()