import socket, sys, threading

# GLOBAL VARIABLES
HOST = socket.gethostname()
IP = socket.gethostbyname(HOST)
PORT = 1234
connections = []

def print_prompt(name):
    print(f"{name} > ", end="", flush=True)
    
# SOCKET INITIALIZATION
def create_soc(hostname, port):
    soc = socket.socket()
    soc.bind((hostname, port))
    print(f"{hostname} ({IP}) ACTIVE ON PORT {PORT}")
    
    soc.listen()
    print("Waiting for connections...")
    
    while True:
        client_conn, client_address = soc.accept()
        threading.Thread(target=handling_connection, args=(client_conn,client_address)).start() # Create separate thread for each connection
        connections.append(client_conn)
    

# BROADCAST MESSAGE TO ALL CONNECTED CLIENTS
def broadcast_message(message, sender_connection):
    for conn in connections:
        if conn != sender_connection:  # Avoid sending the message back to the sender
            try:
                conn.send(message.encode())
            except Exception as e:
                print(f"Error broadcasting message to a client: {e}")
                connections.remove(conn)  # Remove connection if sending fails

# SENDING MESSAGES TO THE CLIENT
def send_message(server_name):
    try:
        while True:
            server_message = input()
            if server_message:
                message = f"{HOST} > {server_message}"
                broadcast_message(message, None)
                print_prompt(server_name)
    except Exception as e:
        print(f"Error sending message to client: {e}")
        
# RECEIVING MESSAGES FROM THE CLIENT
def receive_message(connection, client_name, address):
    try:
        while True:
            client_message = connection.recv(1024)
            if client_message:
                message = f"{client_name} > {client_message.decode()}"
                sys.stdout.write("\r" + " " * 80 + "\r")  # Clear the current line
                print(message) 
                broadcast_message(message, connection)  # Broadcast to other clients
                print_prompt(HOST)  # Show server prompt after displaying message
            else:
                break
    except Exception as e:
        print(f"Error handling client {address}: {e}")
    

# HANDLING CLIENT CONNECTIONS
def handling_connection(connection, address):
    # connection.setblocking(False)
    try:
        client_name = connection.recv(1024).decode()
        connection.send(HOST.encode())  # Send host name to client
        sys.stdout.write("\r" + " " * 80 + "\r")  # Clear the current line
        print(f"{client_name} has joined the chat!")
        broadcast_message(f"{client_name} has joined the chat!", connection)
        
        print_prompt(HOST)  # Show prompt before accepting input
        
        # Start threads for receiving and sending messages
        threading.Thread(target=receive_message, args=(connection, client_name, address)).start()
        threading.Thread(target=send_message, args=(HOST,)).start()

    except Exception as e:
        print(f"Error handling client {address}: {e}")
        connections.remove(connection)
        connection.close()
        
    
# MAIN FUNCTION
if __name__ == "__main__":
    create_soc(HOST, PORT)


