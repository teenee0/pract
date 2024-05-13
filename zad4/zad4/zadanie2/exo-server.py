import socket
import threading

def client_thread(conn, addr):
    print(f"Connected to {addr}")

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.send(data.upper())
    except ConnectionError:
        print(f"Connection error with {addr}. Client disconnected.")

    print(f"Connection with {addr} closed.")
    conn.close()

def run_server():
    sock = socket.socket()
    sock.bind(('', 9090))
    sock.listen(0)

    print("Server started. Waiting for connections...")

    try:
        while True:
            conn, addr = sock.accept()
            thread = threading.Thread(target=client_thread, args=(conn, addr))
            thread.start()
    except KeyboardInterrupt:
        print("Server shutting down.")
    
    sock.close()

if __name__ == "__main__":
    run_server()