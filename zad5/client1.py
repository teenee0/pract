import socket

def power(a, b, c):
    x = 1
    y = a
    while b > 0:
        if b % 2 == 1:
            x = (x * y) % c
        y = (y * y) % c
        b = b // 2
    return x % c

def main():
    host = '127.0.0.1'
    port = 12345

    client_socket = socket.socket()
    client_socket.connect((host, port))

    q, alpha, b_private, b_public = [int(x) for x in client_socket.recv(1024).decode().split(',')]
    print("Получены q, alpha, b_public")

    a_public = power(alpha, b_private, q)
    print("Отправка a_public серверу")
    client_socket.sendall(f"{a_public}".encode())

    s_key = power(b_public, b_private, q)
    print("Секретный ключ:", s_key)

    client_socket.close()

if __name__ == '__main__':
    main()