import socket

def scan_ports(host):
    for port in range(1000, 2000):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"Port {port} is open")
        else:
            print(f"port {port} is closed :(")
        sock.close()

if __name__ == "__main__":
    target = input("Введите имя хоста/IP-адрес для сканирования: ")
    if not target:
        target = "127.0.0.1"
    scan_ports(target)