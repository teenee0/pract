import socket

host = str(input("Введите адрес хоста (например, 127.0.0.1): "))
host = host if len(host) < 8 else "127.0.0.1"
try:
    port = int(input("Введите номер порта (например, 12345): "))
    port = port if 1000 < port < 2**16-1 else 9090
except ValueError:
    port = 9090
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

while True:
    message = input("Введите сообщение для сервера: ")
    if message == "exit":
        break
    client_socket.send(message.encode())
    data = client_socket.recv(1024)
    print("Получено от сервера:", data.decode())

client_socket.close()