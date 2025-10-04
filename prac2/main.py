from http.server import HTTPServer
from handlers import *

address = 'localhost'
port = 8000
server = HTTPServer((address, port), MyHandler) # поднимаем сервер на 8000 порту
print(f"Сервер запущен на {address}:{port}")
server.serve_forever() # говорит серверу - обрабатывать запросы клиентов до явного вызова метода server

# Итого: сервер запускается на 8000 порту, GET и POST выводятся в консоль, HTML страницы выводятся, данные в форме сохраняются в файле.
