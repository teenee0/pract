import socket
import logging

logging.basicConfig(filename='server_log.txt', level=logging.INFO) 

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(0)
conn, addr = sock.accept()
logging.info(f"Connection with {addr}")

msg = ''

while True:
    data = conn.recv(1024)
    if not data:
        break
    msg += data.decode()
    conn.send(data)

logging.info(f"Received message: {msg}")

conn.close()