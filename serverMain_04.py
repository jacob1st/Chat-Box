import socket
import threading

ADDR = "192.168.1.121"
PORT = 6666
HEADER = 64
FORMAT = 'utf-8'

class Client:
    def __init__(self, client_conn, client_address, nickname):
        self.my_client_conn = client_conn
        self.my_client_address = client_address
        self.my_nickname = nickname

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ADDR, PORT))

clients_list = list()

def handle_client(client_conn, client_addr):
    new_client = Client(client_conn, client_addr, len(clients_list))
    for clients in clients_list:
        clients.my_client_conn.send(f"(New user ({new_client.my_nickname}) has connected to chat)".encode(FORMAT))
    clients_list.append(new_client)
    print(f"New user connected from {client_addr}")
    connected = True
    while connected:
        msg_length = client_conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            actual_message = client_conn.recv(msg_length).decode(FORMAT)
            if actual_message == "!DISCONNECT":
                client_conn.send("!".encode(FORMAT))
                connected = False
            if actual_message.startswith("nickname="):
                if actual_message[9] == "!":
                    client_conn.send("(Nicknames cannot start with !)".encode(FORMAT))
                    print(client_addr, " tried changing nickname to a name starting with !")
                else: 
                    print(new_client.my_nickname, " from ", client_addr, " changed their nickname to ", actual_message[9:])
                    for clients in clients_list:
                        clients.my_client_conn.send(f"({new_client.my_nickname} has changed their nickname to {actual_message[9:]})".encode(FORMAT))
                    new_client.my_nickname = actual_message[9:]
        
            print(f"{client_addr} says {actual_message} to everyone.")
            for clients in clients_list:
                clients.my_client_conn.send(f"{new_client.my_nickname} >> \"{actual_message}\" (to everyone.)".encode(FORMAT))

    clients_list.remove(new_client)
    client_conn.close()

def end_server():
    while True:
        stop_server = input()
        if stop_server == "!QUIT":
            print("Closing all connections and exiting...")
            for i in clients_list:
                i.my_client_conn.send("Server [shutting down] uexpectedly. Please close down chat and try again later.".encode(FORMAT))
                i.my_client_conn.close()
                print("Successfully closed one connection.")
            server.close()
            break
            
def start_server():
    server.listen()
    print(f"Server [listening] on {ADDR}:{PORT}...")
    closingThread = threading.Thread(target=end_server)
    closingThread.start()
    while True:
        try:
            client_conn, client_addr = server.accept()
        except OSError:
            break
        thread = threading.Thread(target=handle_client, args=(client_conn,client_addr,))
        thread.start()
        print(f"{int((threading.active_count()-2))} active connections")

print(f"Chat is [Starting] on {ADDR}:{PORT}")
start_server()
