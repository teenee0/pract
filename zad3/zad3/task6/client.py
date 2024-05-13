import socket
from time import sleep

class MySocket(socket.socket):
    def __init__(self, *args, **kwargs):
        super(MySocket, self).__init__(*args, **kwargs)

    def send_msg(self, msg):
        msg_bytes = msg.encode()
        msg_length = len(msg_bytes)
        header = f"{msg_length:<10}".encode()
        self.sendall(header + msg_bytes)

    def recv_msg(self):
        header = self.recv(10)
        if not header:
            return None

        msg_length = int(header.decode().strip())
        msg = b''
        while len(msg) < msg_length:
            chunk = self.recv(min(msg_length - len(msg), 1024))
            if not chunk:
                break
            msg += chunk

        return msg.decode()

        
sock = MySocket()
sock.setblocking(1)
sock.connect(('127.0.0.1', 9090))
while True:
    msg = input()
    sock.send_msg(msg)

    data = sock.recv_msg()
    print(data)
