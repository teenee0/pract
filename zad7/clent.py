import socket

def main():
    HOST = 'localhost'
    PORT = 9090

    while True:
        sock = socket.socket()
        sock.connect((HOST, PORT))

        request = input('myftp@shell$ ')
        sock.send(request.encode())

        if request == 'exit':
            break

        response = sock.recv(1024).decode()
        print(response)

        sock.close()

if __name__ == "__main__":
    main()
