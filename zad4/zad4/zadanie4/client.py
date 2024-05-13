import socket
from time import sleep
for i in range(100):
    sock = socket.socket()
    sock.setblocking(1)
    sock.connect(('127.0.0.1', 12345))
    while True:
        break