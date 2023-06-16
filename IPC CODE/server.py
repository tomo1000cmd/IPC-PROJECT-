import socket
import random
import time


# Server configuration
HOST = 'localhost'
PORT = 8888

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(1)

print("Server started. Waiting for connections...")

# Accept a client connection
client_socket, client_address = server_socket.accept()
print("Client connected:", client_address)

# Maximum spaces for each section
max_spaces = [50, 20, 20]

while True:
    start_time = time.time()
    # Generate random available spaces for each section
    available_spaces = [random.randint(0, max_spaces[i]) for i in range(3)]
    
    
    # Concatenate the available spaces as a single string separated by commas
    spaces_str = ",".join(str(space) for space in available_spaces)
    
    # Send the available spaces data to the client
    client_socket.sendall(spaces_str.encode())
    end_time = time.time()
     # Calculate communication speed
    speed = end_time - start_time
    # Sleep for 1 second
    time.sleep(5)

# Close the client connection
    client_socket.close()

# Close the server socket
    server_socket.close()
