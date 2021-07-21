import socket
import threading

PORT = 6666
ADDR = "192.168.1.121"
FORMAT = 'utf-8'
HEADER = 64

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ADDR, PORT))


def listen_for_msg():
    while threading.active_count() == 3:
        print("\n" + client.recv(2048).decode(FORMAT) +"\nMessage: ")

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def sending_messages():
    while True:
        myMessage = input("Message: ")
        send(myMessage)
        if myMessage == "!DISCONNECT":
            break

def start():
    send_thread = threading.Thread(target=sending_messages)
    send_thread.start()

    recv_thread = threading.Thread(target=listen_for_msg)
    recv_thread.start()

start()
