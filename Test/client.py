import socket
import sys
import time
from datetime import datetime
import threading

def connect_to_server(host_address, port_number):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host_address, port_number))
    return client_socket

def display_connection_details(client_socket):
    print("\n     [ Secure Connection:", client_socket.getsockname(), "]",
          datetime.now().strftime("%a, %d-%b-%Y/%H:%M:%S"), "(" + time.tzname[0] + ") ")
    time.sleep(2)

def handle_server_response(client_socket):
    while True:
        response_data = client_socket.recv(1024)
        if not response_data:
            break
        sys.stdout.write(response_data.decode())
        sys.stdout.flush()

def send_client_message(client_socket):
    while True:
        user_input = input()
        client_socket.sendall(user_input.encode())

def main():
    try:
        default_host = "127.0.0.1"
        default_port = 1025

        client_socket = connect_to_server(default_host, default_port)

        if client_socket:
            display_connection_details(client_socket)

            # Create a thread for handling server responses
            response_thread = threading.Thread(target=handle_server_response, args=(client_socket,))
            response_thread.daemon = True
            response_thread.start()

            send_client_message(client_socket)
        else:
            print("\n [Client Connection] Error Occurred \n")
    except KeyboardInterrupt:
        exit()

if __name__ == "__main__":
    main()
