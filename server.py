import socket
import threading

# Server configuration
HOST = socket.gethostname()
PORT = 9999
LOG_FILE = "server_log.txt"
clients = {}  # Dictionary to store client connections

def log_message(message):
    with open(LOG_FILE, "a") as log:
        log.write(message + "\n")
    print(message)

def handle_client(client_socket, client_address):
    pass

def process_request(client_socket, client_address, data):
    parts = data.split()
    command = parts[0].upper()

    #1
    if command == "STORE" and len(parts) > 2:
        pass

    #2
    elif command == "RETRIEVE" and len(parts) == 2:
        pass

    #3
    elif command in ["ADD", "MULTIPLY", "DIVIDE", "SUBTRACT"] and len(parts) == 3:
        pass

    #4
    elif command == "MESSAGE" and len(parts) > 2:
        pass

    return "ERROR: Invalid command."

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    startup_message = f"Server listening on port {PORT}"
    log_message(startup_message)
    print(startup_message)

    while True:
        client_socket, client_address = server.accept()
        username = client_socket.recv(1024).decode()
        clients[username] = client_socket
        
        connection_msg = f"{username} connected from {client_address}"
        log_message(connection_msg)
        print(connection_msg)

        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

if __name__ == "__main__":
    start_server()
