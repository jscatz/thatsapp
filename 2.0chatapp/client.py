import socket
import threading

# Client information
HOST = input("HOST: ")  # Server's IP address
PORT = 9009

# Function to receive messages from the server
def receive():
    while True:
        try:
            # Receive message from the server
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            # Close the connection on error
            print("An error occurred!")
            client.close()
            break

# Function to send messages to the server
def send():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf-8'))

# Get the nickname for the client
nickname = input("Choose your nickname: ")

# Connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Start threads for receiving and sending messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()

send_thread = threading.Thread(target=send)
send_thread.start()
