import socket
import threading

def scan_ports(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((host, port))
    if result == 0:
        print(f"Port {port} is open")
    sock.close()

def start_scan(host):
    threads = []
    for port in range(1, 1025):
        thread = threading.Thread(target=scan_ports, args=(host, port))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    target = input("Введите имя хоста/IP-адрес для сканирования: ")
    if not target:
        target = "127.0.0.1"
    start_scan(target) 