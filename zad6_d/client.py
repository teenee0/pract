import http.client

def send_message_to_server(message):
    server_address = "localhost"
    server_port = 80
    url = "/"

    connection = http.client.HTTPConnection(server_address, server_port)
    connection.request("POST", url, message)
    response = connection.getresponse()
    print(response.read().decode())
    connection.close()

if __name__ == "__main__":
    user_message = input("Введите ваше сообщение: ")
    send_message_to_server(user_message)