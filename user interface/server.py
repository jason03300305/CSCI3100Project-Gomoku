import socket
import threading
import pickle
import numpy

# Create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server.bind(('10.13.80.3', 5555))

# Start listening for incoming connections
server.listen(4)
print("Waiting for a connection, Server Started")
# Keep a list of all connected clients
clients = []
#board = numpy.zeros((19,19), dtype = int)
def handle_client(client):
    #client.send(pickle.dumps(board))
    while True:
        # Receive data from the client
        data = client.recv(2048*100)
        reply_board = pickle.loads(data)
        if not data:
            print("Disconnected")
            break
        else:
            print("Received: ", reply_board)
            print("Sending : ", reply_board)

        # Send the data to all connected clients
        for c in clients:
            c.send(data)

    # Remove the client from the list of connected clients
    print("Lost connection", client)
    clients.remove(client)
    client.close()

while True:
    # Accept a new client connection
    client, addr = server.accept()
    print(f"Accepted connection from {addr}")

    # Add the client to the list of connected clients
    clients.append(client)

    # Start a new thread to handle the client
    threading.Thread(target=handle_client, args=(client,)).start()