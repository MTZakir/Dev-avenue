import socket
import time
from datetime import datetime
import threading

def host_server(port_number):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port_number))
    server_socket.listen()

    print("\n     [ Local Server: Online (", server_socket.getsockname(), ") ",
          datetime.now().strftime("%a, %d-%b-%Y/%H:%M:%S"), " (", time.tzname[0], ") ] ")

    connected_clients = []

    while True:
        client_socket, client_address = server_socket.accept()
        connected_clients.append(client_socket)
        print("\n[*] Client Connected:", client_address)

        client_thread = threading.Thread(target=handle_client_connection, args=(client_socket, connected_clients))
        client_thread.start()

def handle_client_connection(client_socket, connected_clients):
    client_name = get_client_name(client_socket)

    if client_name:
        process_client_message(client_name, client_socket, connected_clients)

def get_client_name(client_socket):
    client_socket.sendall(b"Name: ")
    client_name = client_socket.recv(1024).decode().strip()

    if client_name:
        print("User:", client_name)
        print("Host-Port:", client_socket.getpeername())
        client_socket.sendall(b"\n          +--------------------------------------------+\n"
                              b"          | Welcome To MyChat (v1.0) [UID: " + str(client_socket.fileno()).encode() + b"] |\n"
                              b"          +--------------------------------------------+\n")
        time.sleep(2)
        return client_name
    else:
        client_socket.sendall(b"\n [Server] Invalid Name \n")
        return None

def process_client_message(client_name, client_socket, connected_clients):
    for client_output in connected_clients:
        if client_output != client_socket:
            client_output.sendall(b"\n\n [Server] " + client_name.encode() + b" is Online "
                                   b"(" + datetime.now().strftime("%H:%M").encode() + b")\n")

    while True:
        client_socket.sendall(b"[" + client_name.encode() + b"] ")
        message_line = client_socket.recv(1024).decode().strip()

        if message_line.lower() == "logout":
            print("\n[*] Client Disconnected:", client_name)
            client_socket.sendall(b"\n [Server Disconnected] \n")
            client_socket.sendall(b"Session lasted for: " + str(time.time()).encode() + b" seconds\n")
            break
        else:
            print(" [", datetime.now().strftime("%d/%b/%Y %H:%M:%S"), "] [", client_name, "] ", message_line)

            for client_output in connected_clients:
                if client_output != client_socket:
                    client_output.sendall(b"\n\n[" + client_name.encode() + b"] " + message_line.encode() + b"\n")
                    client_output.sendall(b" " * 20 + b"(Message Received)\n")

            client_socket.sendall(b" " * 20 + b"(Message Delivered)\n")
            time.sleep(0.25)

    for client_output in connected_clients:
        if client_output != client_socket:
            client_output.sendall(b"\n\n [Server] " + client_name.encode() + b" is Offline "
                                   b"(" + datetime.now().strftime("%H:%M").encode() + b")\n")

    connected_clients.remove(client_socket)
    client_socket.close()

def main():
    default_port = 1025
    host_server(default_port)

if __name__ == "__main__":
    main()
