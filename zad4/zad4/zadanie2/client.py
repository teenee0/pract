import socket
from time import sleep

sock = socket.socket()
sock.setblocking(1)
sock.connect(('127.0.0.1', 9090))
while True:
    msg = input("enter message:\n")
    sock.send(msg.encode())
    data = sock.recv(1024)
    print(data.decode())