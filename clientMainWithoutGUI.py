# Works similair to clientMain_02 however there is no GUI application - it still works with the server and can talk to the GUI version
import socket
import threading

# Must change ADDR to the address the server is hosted on
PORT = 6666
ADDR = ""
FORMAT = 'utf-8'
HEADER = 64

# Create a socket obkect named client

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ADDR, PORT))

# a thread to constantly listen for incoming messages
def listen_for_msg():
    while threading.active_count() == 3:
        print("\n" + client.recv(2048).decode(FORMAT) +"\nMessage: ")

# to send a message to the server (not the same as socket.send() which is a method of the socket class)
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

# a thread to listen for input to send to the server
def sending_messages():
    while True:
        myMessage = input("Message: ")
        send(myMessage)
        if myMessage == "!DISCONNECT":
            break

# starts all of our threads
def start():
    send_thread = threading.Thread(target=sending_messages)
    send_thread.start()

    recv_thread = threading.Thread(target=listen_for_msg)
    recv_thread.start()

start()
