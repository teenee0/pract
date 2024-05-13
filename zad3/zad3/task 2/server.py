import socket

host = '127.0.0.1'
try:
    port = int(input("Введите номер порта (например, 12345): "))
    port = port if 1000 < port < 2**16-1 else 9090
except ValueError:
    port = 9090

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)

print("waiting for connections ...")

client_socket, address = server_socket.accept()
print(f"got connection from {address}")

while True:
    data = client_socket.recv(1024)
    if not data:
        break
    print(f"message from {address}: {data.decode()}")
    client_socket.send(data.decode().upper().encode())

client_socket.close()
server_socket.close()