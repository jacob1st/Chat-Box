###IDEAS
# scrollwheel, admin perms, customization

import socket
import threading
import tkinter as tk

PORT = 6666
# Change addr to the adress that the server is being hosted on (e.x. ADDR = "192.168.1.2")
ADDR = ""
FORMAT = 'utf-8'
HEADER = 64

# GUI Screen Dimensions

HEIGHT = 700
WIDTH = 800

# colors used in GUI
black_hexcolor = "#506D05"
darkblue_hexcolor = "#1F208D"
lavander_hexcolor = "#B673E8"

# Client Socket connected to server

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ADDR, PORT))

# Seperate Thread to listen for incoming messages from the server

def listen_for_msg():
    while root.state() == 'normal':
        final_message = client.recv(2048).decode(FORMAT) + "\n"
        if final_message.startswith("!"):
            break
        texts_label['text'] += final_message
        if len(texts_label['text']) > 400:
            texts_label['text'] = final_message

# Encoding and sending a message telling the length for padding and then 
# the actual message (send is a bad name becuase client.send is a built in socket method)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

# The thread looking to send messages

def sending_messages(entry_message):
    send(entry_message)
    entry.delete(0, 'end')
    if entry_message == "!DISCONNECT":
        root.destroy()

# Not really sure why it's a seperate func, but it starts the listening thread

def start():
    recv_thread = threading.Thread(target=listen_for_msg)
    recv_thread.start()

# **Actually creating the GUI**

root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

# Black frame (for entry)
full_frame = tk.Frame(root, bg=black_hexcolor)
full_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

# Blue frame
frame = tk.Frame(root, bg=darkblue_hexcolor)
frame.place(relx=0, rely=0, relwidth=1, relheight=0.9)

#label for messages in Blue Frame
texts_label = tk.Label(frame, bg=darkblue_hexcolor, fg="white", wraplength=600, relief="ridge", font="Calibri 15", anchor="nw", justify="left", border=4)
texts_label.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

# Send button
button = tk.Button(full_frame, text="send", font="Arial 12", bg=lavander_hexcolor, command=lambda: sending_messages(entry.get()))
button.place(relx=.9, rely=0.9, relwidth=.1, relheight=.1)

# Message label
label = tk.Label(full_frame, text="Message: ", relief="raised", bg=lavander_hexcolor, font="Arial 12")
label.place(relx=0, rely=0.9, relwidth=.1, relheight=.1)

# To send message
entry = tk.Entry(full_frame, bg='black', fg='white', relief="ridge", font="Calibri 13", insertbackground='white')
entry.place(relx=0.1, rely=.9, relwidth=.8, relheight=.1) 

start()

root.mainloop()

