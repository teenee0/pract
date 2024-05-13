import socket
import random

def power(a, b, c):
    x = 1
    y = a
    while b > 0:
        if b % 2 == 1:
            x = (x * y) % c
        y = (y * y) % c
        b = b // 2
    return x % c

def generate_key():
    q = random.randint(2, 50)
    alpha = random.randint(2, q-1)
    a_private = random.randint(2, q-1)
    a_public = power(alpha, a_private, q)
    return q, alpha, a_private, a_public

def main():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)

    conn, addr = server_socket.accept()
    print("Соединение установлено с клиентом:", addr)

    q, alpha, a_private, a_public = generate_key()
    print("Отправка q, alpha, a_public клиенту")
    conn.sendall(f"{q},{alpha},{a_private},{a_public}".encode())
    b_public = int(conn.recv(1024).decode())
    s_key = power(b_public, a_private, q)
    print("Секретный ключ:", s_key)

    conn.close()
    server_socket.close()

if __name__ == '__main__':
    main()