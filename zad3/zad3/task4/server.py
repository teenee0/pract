import socket
import logging

port = 9090

while True:
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', port))
        break
    except OSError:
        print(f"Port {port} is already in use, trying another port...")
        port += 1

print(f"Server is listening on port {port}")

server.listen(5)

while True:
    client_socket, address = server.accept()
    msg = ''

    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        msg += data.decode()
        client_socket.send(data)

    logging.info(f"Received message: {msg}")

    client_socket.close()
#C:/Users/PC/AppData/Local/Microsoft/WindowsApps/python3.11.exe d:/programming/pp/zad3/zad3/task4/server.py