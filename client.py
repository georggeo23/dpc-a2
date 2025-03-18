import socket

SERVER_HOST = socket.gethostname()
SERVER_PORT = 9999

def start_client(username):
    """Starts the client and connects to the server."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_HOST, SERVER_PORT))
    
    # Send username for message forwarding
    client.send(username.encode())

    while True:
        command = input("Enter command: ")
        if command.lower() == "exit":
            break
        
        # Handle server response here
        client.send(command.encode())
        response = client.recv(1024).decode()

        if response.startswith("CONTENT"):
            pass
        elif response.startswith("MSG"):
            parts = response.split(" ", 2)
            sender, message = parts[1], parts[2]
            print(f"Message from {sender}: {message}")
        else:
            print("Server:", response)

    client.close()

if __name__ == "__main__":
    username = input("Enter your username: ")
    start_client(username)
