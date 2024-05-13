import socket
import threading

# Класс для сервера чата
class ChatServer:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 5050
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}  # Словарь для хранения подключенных клиентов и их данных
        self.server.bind((self.host, self.port))
        self.server.listen()

    def handle_client(self, client_sock, client_addr):
        while True:
            msg = client_sock.recv(1024).decode()
            if not msg:  # Если сообщение пустое, завершаем обработку клиента
                break
            for client in self.clients:
                if client != client_sock:
                    client.send(f'{self.clients[client_sock]}: {msg}'.encode())

    def start(self):
        print("Chat server is running...")
        while True:
            client_sock, client_addr = self.server.accept()
            client_name = client_sock.recv(1024).decode()
            self.clients[client_sock] = client_name
            print(f"{client_name} connected from {client_addr}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_sock, client_addr))
            client_thread.start()

chat_server = ChatServer()
chat_server.start()