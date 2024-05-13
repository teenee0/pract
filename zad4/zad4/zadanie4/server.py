import socket
import threading
import os
import sys

class ServerThread(threading.Thread):
    def __init__(self, port):
        super().__init__()
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', port))
        self.server_socket.listen(5)
        self.running = True

    def run(self):
        while self.running:
            sock, address = self.server_socket.accept()
            print(f"got connection from {address}")
            with open("logs.txt", "a") as f:
                f.write(f"got connection from {address}\n")
            
    def stop(self):
        self.running = False
        self.server_socket.close()

def main():
    port = 12345
    server_thread = ServerThread(port)
    server_thread.start()
    print("Server is running ...")

    while True:
        command = str(input("Enter command: \n"))
        if command == 'shutdown':
            #server_thread.stop()
            break
        elif command == 'pause':
            server_thread.running = False
        elif command == 'resume':
            server_thread.running = True
        elif command == 'show logs':
            with open('logs.txt', 'r') as f:
                print(f.read())
        elif command == 'clear logs':
            open('logs.txt', 'w').close()
            print("Логи очищены.")
        elif command == 'clear id file':
            if os.path.exists('id.txt'):
                with open("id.txt", "w"):
                    pass
                print("Файл идентификации очищен.")
            else:
                print("Файл идентификации не найден.")
        else:
            print("Неизвестная команда")

if __name__ == "__main__":
    main()