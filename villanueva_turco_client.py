import socket, sys, time, threading

# GLOBAL VARIABLES
HOST = socket.gethostname()
IP = socket.gethostbyname(HOST)
PORT = 1234

# Set socket options to keep the connection alive
def setup_socket_options(soc):
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

def print_prompt(name):
    print(f"{name} > ", end="", flush=True)

# SENDING MESSAGES
def send_message(connection, client_name):
    try:
        while True:
            client_message = input()
            if client_message:
                connection.send(client_message.encode())
                print_prompt(client_name)
    except Exception as e:
        print(f"Error sending message to server: {e}")
        connection.close()

# RECEIVING MESSAGES
def receive_message(connection, host_name, client_name):
    try:
        while True:
            server_message = connection.recv(1024)
            if server_message:
                sys.stdout.write("\r" + " " * 80 + "\r")  # Clear out lines in cmd
                print(server_message.decode())
                print_prompt(client_name)
            else:
                break
    except Exception as e:
        print(f"Error handling client {connection}: {e}")
        connection.close()

def create_client(PORT):
    server_host = input("Enter server's IP address: ")
    client_name = input("Enter client name: ")

    print(f"Trying to connect to the server: {server_host} on PORT {PORT}")

    # INITIALIZING SOCKET AND CONNECTING TO SERVER
    while True:
        try:
            soc = socket.socket()
            soc.connect((server_host, PORT))
            soc.send(client_name.encode())  # Send client name to server
            host_name = soc.recv(1024)
            host_name = host_name.decode()
            print("Welcome to the chat!")
            print_prompt(client_name)  # Show prompt before accepting input

            # Start threads for receiving and sending messages
            threading.Thread(target=receive_message, args=(soc, host_name, client_name)).start()
            threading.Thread(target=send_message, args=(soc, client_name)).start()
            break  # Exit the loop once connected successfully

        except (socket.error, ConnectionRefusedError) as e:
            print(f"Connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)  # Wait before retrying to reconnect

# MAIN FUNCTION
if __name__ == "__main__":
    create_client(PORT)
