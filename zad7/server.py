import os
import socket
import shutil
import logging

def setup_logging():
    logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

def log_action(action):
    logging.info(action)

def process(request, client_dir):
    if request == 'pwd':
        return client_dir
    elif request == 'ls':
        return '; '.join(os.listdir(client_dir))
    elif request.startswith('cd'):
        path = request.split()[1]
        new_dir = os.path.join(client_dir, path)
        return f'Directory changed to {os.getcwd()}', new_dir
    elif request.startswith('mkdir'):
        folder_name = request.split()[1]
        os.mkdir(os.path.join(client_dir, folder_name))
        return f'Folder {folder_name} created'
    elif request.startswith('rmdir'):
        folder_name = request.split()[1]
        shutil.rmtree(os.path.join(client_dir, folder_name))
        return f'Folder {folder_name} deleted'
    elif request.startswith('rmfile'):
        file_name = request.split()[1]
        os.remove(os.path.join(client_dir, file_name))
        return f'File {file_name} deleted'
    elif request.startswith('rename'):
        old_name, new_name = request.split()[1:]
        os.rename(os.path.join(client_dir, old_name), os.path.join(client_dir, new_name))
        return f'File {old_name} renamed to {new_name}'
    elif request.startswith('copyto'):
        file_name = request.split()[1]
        shutil.copy(os.path.join(client_dir, file_name), file_name)
        return f'File {file_name} copied to client'
    elif request.startswith('copyfrom'):
        file_name = request.split()[1]
        shutil.copy(file_name, os.path.join(client_dir, file_name))
        return f'File {file_name} copied to server'
    elif request.startswith('readfile'):
        file_name = request.split()[1]
        with open(os.path.join(client_dir, file_name), 'r') as file:
            return file.read()
    elif request == 'exit':
        return 'exit'
    else:
        return 'bad request'

def read_credentials(file_path):
    credentials = {}
    with open(file_path, 'r') as file:
        for line in file:
            username, password = line.strip().split()
            credentials[username] = password
    return credentials

def write_credentials(file_path, credentials):
    with open(file_path, 'w') as file:
        for username, password in credentials.items():
            file.write(f"{username} {password}\n")
def check_credentials(username, password, credentials):
    if username in credentials and credentials[username] == password:
        return True
    return False
def register_user(username, password, credentials_file, server_dir):
    credentials = read_credentials(credentials_file)
    if username in credentials:
        return f'User {username} already exists'
    credentials[username] = password
    write_credentials(credentials_file, credentials)
    user_dir = os.path.join(server_dir, username)
    if not os.path.exists(user_dir):
        os.mkdir(user_dir)
    return f'User {username} registered successfully'


def auth_user(username, password, credentials_file):
    credentials = read_credentials(credentials_file)
    if username in credentials and credentials[username] == password:
        return f'User {username} logged in successfully'
    else:
        return 'Invalid username or password'

def main():
    HOST = 'localhost'
    PORT = 9090
    server_dir = 'C:\\Users\\Asus\\Desktop\\практикум зачет\\server_directory'
    credentials_file = 'credentials.txt'
    client_dir = None

    setup_logging()

    sock = socket.socket()
    sock.bind((HOST, PORT))
    sock.listen()

    print(f"Server is listening on port {PORT}")
    
    
    while True:
        conn, addr = sock.accept()
        print(f"Connected by {addr}")

        request = conn.recv(1024).decode()
        print(f"Received request: {request}")

        log_action(f"Received request: {request}")

        if request.startswith('login'):
            username, password = request.split()[1:]
            response = auth_user(username, password, credentials_file)
            client_dir = os.path.join(server_dir, username) if 'logged in successfully' in response else None
            response += client_dir
        elif request.startswith('register'):
            username, password = request.split()[1:]
            response = register_user(username, password, credentials_file, server_dir)
            client_dir = os.path.join(server_dir, username) if 'registered successfully' in response else None
        else:
            if client_dir != None:
                response = process(request, client_dir)
            else:
                response = process(request, server_dir)

        

        conn.send(response.encode())

        log_action(f"Sent response: {response}")

        if response == 'exit':
            break

        conn.close()

    sock.close()

if __name__ == "__main__":
    main()


