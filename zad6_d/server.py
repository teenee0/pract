from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            with open("index.html", "r") as file:
                content = file.read()
        except FileNotFoundError:
            content = "Файл index.html не найден"
        except Exception as e:
            content = f"Ошибка при чтении файла: {str(e)}"

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        try:
            with open("index.html", "w") as file:
                file.write(post_data)
            response_message = "Данные успешно записаны"
        except Exception as e:
            response_message = f"Ошибка при записи данных в файл: {str(e)}"

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(response_message.encode())

def run_server():
    with HTTPServer(('localhost', 80), SimpleHTTPRequestHandler) as httpd:
        print("Сервер запущен на порту 80...")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()