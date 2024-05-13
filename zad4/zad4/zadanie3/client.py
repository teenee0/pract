import socket
from time import sleep
import threading
def listen(socket):
    while True:
        data = socket.recv(1024)
        if not data:
            break
        print(data.decode())

def chat(socket):
    while True:
        msg = input("Enter your message: ")
        if not msg:
            break
        sock.send(msg.encode())

sock = socket.socket()
sock.setblocking(1)
sock.connect(('127.0.0.1', 5050))
threading.Thread(target=listen, args=[sock]).start()
threading.Thread(target=chat, args=[sock]).start()