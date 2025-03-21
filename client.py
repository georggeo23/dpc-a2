import socket
import threading

SERVER_HOST = socket.gethostname()
SERVER_PORT = 9999

# Continuously listens for incoming messages from the server.
def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode()
            if message.startswith("MSG"):
                parts = message.split(" ", 2)
                sender, text = parts[1], parts[2]
                print(f"\n📩 Message from {sender}: {text}\n", end="")
        except Exception:
            print("Error receiving a message")

# Starts the client and connects to the server.
def start_client(username):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_HOST, SERVER_PORT))
    
    # Send username for message forwarding
    client.send(username.encode())

    # Separate thread for receiving messages
    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()
    
    while True:
        try:
            command = input("Enter command: ")
            if command.lower() == "exit":
                break
            
            # Handle server response here
            client.send(command.encode())
            response = client.recv(1024).decode()
            
            print("Server:", response)

        except:
            break

    client.close()

if __name__ == "__main__":
    username = input("Enter your username: ")
    start_client(username)
