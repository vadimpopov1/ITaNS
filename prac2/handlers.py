from http.server import BaseHTTPRequestHandler
import urllib.parse
from utils import save_to_json

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/': # Обрабатываем GET запросы.
            self.send_page("Главная страница", "Добро пожаловать на сайт!")
        elif self.path == '/about':
            self.send_page("О нас", "Информация о компании")
        elif self.path == '/contact':
            self.send_page("Контакты", "Email: info@example.com")
        elif self.path == '/services':
            self.send_page("Услуги", "Наши услуги: Веб-разработка, Консультации, Поддержка")
        elif self.path == '/feedback':
            self.send_form()
        elif self.path == '/success':
            self.send_success_page()
        else:
            self.send_404()

    def do_POST(self):
        if self.path == '/submit': # Обрабатываем POST запрос, который появляется после заполнения формы.
            self.handle_form_submission()

    def send_form(self): # /feedback
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        html = '''
        <html>
            <head><title>Форма обратной связи</title></head>
            <body>
                <h1>Обратная связь</h1>
                <form action="/submit" method="post">
                    <p>
                        <label>Имя:</label><br>
                        <input type="text" name="name" required>
                    </p>
                    <p>
                        <label>Email:</label><br>
                        <input type="email" name="email" required>
                    </p>
                    <p>
                        <label>Тема сообщения:</label><br>
                        <textarea name="theme" rows="1" cols="50"></textarea>
                    </p>
                    <p>
                        <label>Сообщение:</label><br>
                        <textarea name="message" rows="5" cols="50"></textarea>
                    </p>
                    <p>
                        <button type="submit">Отправить</button>
                    </p>
                </form>
            </body>
        </html>
        '''

        self.wfile.write(html.encode('utf-8'))

    def send_success_page(self): # /success
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        html = f'''
        <html>
            <head><title>Успешно</title></head>
            <body>
                <h1>Форма успешно отправлена.</h1>
                <p>
                    <a href="/">Вернуться назад</a>
                </p>
            </body>
        </html>
        '''

        self.wfile.write(html.encode('utf-8'))

    def send_page(self, title, content): # / , /about, /services, /contact, /feedback
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        html = f'''
        <html>
            <head><title>{title}</title></head>
            <body>
                <nav>
                    <a href="/">Главная</a> |
                    <a href="/about">О нас</a> |
                    <a href="/services">Услуги</a> |
                    <a href="/contact">Контакты</a> |
                    <a href="/feedback">Обратная связь</a>
                </nav>
                <h1>{title}</h1>
                <p>{content}</p>
            </body>
        </html>
        '''

        self.wfile.write(html.encode('utf-8'))

    def handle_form_submission(self):
        # Получаем длину тела запроса из заголовков
        content_length = int(self.headers['Content-Length'])

        # Читаем тело запроса (данные формы) как байты и декодируем в строку
        post_data = self.rfile.read(content_length).decode('utf-8')

        form_data = urllib.parse.parse_qs(post_data)

        # Валидация обязательных полей (проверка на сервере)
        if not form_data.get('name') or not form_data.get('email'):
            self.send_error(400, "Имя и email обязательны")
            return

        print(f"Получены данные: {form_data}")

        save_to_json(form_data)

        self.send_response(302)
        self.send_header('Location', '/success')
        self.end_headers()

    def send_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        self.wfile.write('<h1>404 - Страница не найдена</h1>'.encode('utf-8'))