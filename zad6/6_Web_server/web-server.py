import socket
import os
import datetime
import configparser
from threading import Thread
from logger import log

def get_settings():
    config = configparser.ConfigParser()
    config.read("settings.ini")
    return int(config.get("SETTINGS", "PORT")), config.get("SETTINGS", "ROOT_DIR"), int(config.get("SETTINGS", "MAX_SIZE"))

def read_file(filename):
    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        mode = "rb"
    else:
        mode = "r"
    with open(filename, mode) as file:
        return file.read()

def generate_http_response(status_code, content_type, content):
    current_time = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    http_response = f"""\
HTTP/1.1 {status_code}
Date: {current_time}
Server: SelfMadeServer v0.0.1
Content-Type: {content_type}
Content-Length: {len(content)}
Connection: close

"""
    if content_type == "text/html":
        return http_response.encode() + content.encode()
    else:
        return http_response.encode() + content

def handle_request(client_socket, client_address, request_data):
    lines = request_data.split('\n')
    request_line = lines[0].strip()
    path = request_line.split()[1]
    file_path = os.path.join(root_dir, path.lstrip('/'))
    print(file_path)
    if file_path.endswith('.html') or file_path.endswith('.css') or file_path.endswith('.js'):
        content_type = 'text/html'
    elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
        content_type = 'image/jpeg'
    elif file_path.endswith('.png'):
        content_type = 'image/png'
    errors = ""
    try:
        if path.split(".")[-1] in ["html", "css", "js", "jpg", "jpeg", "png"]:
            file_content = read_file(file_path)
            http_response = generate_http_response("200 OK", content_type, file_content)
        else:
            raise ValueError("Restricted file type")
    except ValueError as e:
        errors = e 
        http_response = generate_http_response("403", "text/html", "403")
    except Exception as e:
        errors = e
        http_response = generate_http_response("404 Not Found", "text/html", "404 Not Found")
    log(client_address, f"filename='{file_path}' errors={errors}")
    client_socket.send(http_response)

port, root_dir, max_size = get_settings()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', port))
server_socket.listen(5)
print(f"Server is listening on port {port}...")
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")
    request_data = client_socket.recv(max_size).decode('utf-8')
    tread = Thread(target=handle_request, args=(client_socket, client_address, request_data))
    tread.start()