import os
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
    log_message(f"New connection from {client_address}")
    while True:
        try:
            request = client_socket.recv(1024).decode()
            if not request:
                break

            log_message(f"Received from {client_address}: {request}")
            response = process_request(client_address, client_socket, request)
            client_socket.send(response.encode())
        
        except Exception as e:
            log_message(f"Error handling client {client_address}: {e}")
            break
    
    client_socket.close()
    log_message(f"Connection closed for {client_address}")

def process_request(client_address, client_socket, data):
    parts = data.split(maxsplit=2)
    print(parts)
    command = parts[0].upper()

    # storage_dir = "server_files"
    # os.makedirs(storage_dir, exist_ok=True)

    #1
    if command == "STORE" and len(parts) > 2:
        filename, data = parts[1], parts[2]
        #file_path = os.path.join(storage_dir, filename)

        with open(filename, "w") as f:
            f.write(data)
        return "File stored successfully."

    #2
    elif command == "RETRIEVE" and len(parts) == 2:
        filename = parts[1]
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = f.read()
            log_message("File retrieved")
            return data
        else:
            return "File not found."

    #3
    elif command in ["ADD", "MULTIPLY", "DIVIDE", "SUBTRACT"] and len(parts) == 3:
        try:
            num1, num2 = float(parts[1]), float(parts[2])
            if command == "ADD":
                return f"RESULT {num1 + num2}"
            elif command == "MULTIPLY":
                return f"RESULT {num1 * num2}"
            elif command == "DIVIDE":
                return f"RESULT {num1 / num2}" if num2 != 0 else "ERROR: Division by zero"
            elif command == "SUBTRACT":
                return f"RESULT {num1 - num2}"
        except ValueError:
            return "ERROR: Invalid numbers."

    #4
    elif command == "MESSAGE" and len(parts) > 2:
        recipient, message = parts[1], " ".join(parts[2:])
        if recipient in clients:
            clients[recipient].send(f"MSG {client_address} {message}".encode())
            return "Message sent."
        else:
            return "ERROR: Recipient not connected."

    return "ERROR: Invalid command."

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    startup_message = f"Server listening on port {PORT}"
    log_message(startup_message)

    while True:
        client_socket, client_address = server.accept()
        username = client_socket.recv(1024).decode()
        clients[username] = client_socket
        
        connection_msg = f"{username} connected from {client_address}"
        log_message(connection_msg)

        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

if __name__ == "__main__":
    start_server()
