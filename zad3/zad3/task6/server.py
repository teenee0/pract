import socket
import logging

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

# Пример использования
def main():
    sock = MySocket()
    # sock.connect(('127.0.0.1', 9090))
    # ms = "Hi!"
    # sock.send_msg(ms)
    sock.bind(("", 9090))
    sock.listen(0)
    conn, addr = sock.accept()
    logging.info(f"Connection established with {addr}")

    msg = ''

    while True:
        data = conn.recv(1024)
        if not data:
            break
        msg += data.decode()
        conn.send(data)

    logging.info(f"Received message: {msg}")

    conn.close()
main()