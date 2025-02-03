import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("\n\n[ChatConsumer] Клиент подключен\n\n")
        await self.accept()

    def get_user_data(self):
        # Получаем заголовки
        headers = {key.decode(): value.decode() for key, value in self.scope["headers"]}
        print(f"\n\n[ChatConsumer] Заголовки: {headers}\n")

        # Извлекаем куки из заголовков
        raw_cookies = headers.get("cookie", "")
        cookies = {k: v for k, v in [cookie.split("=") for cookie in raw_cookies.split("; ") if "=" in cookie]}
        print(f"[ChatConsumer] Cookies: {cookies}\n")
        return cookies

    async def receive(self, text_data=None, bytes_data=None):
        print(f"\n\n[ChatConsumer] RAW text_data: {text_data}\n\n")
        try:
            data = json.loads(text_data)
            message = data.get("message", "").strip()

            if not message:
                print("\n\n[ChatConsumer] Пустое сообщение, игнорируем.\n\n")
                return

            print('==' * 60)
            print(f"\n\n[ChatConsumer] Получено сообщение: {message}")
            cookies = self.get_user_data()
            context = {'message': message, 'cookies': cookies}
            html_data = render_to_string('app/components_html/htmx/test.html', context)
            # response_utf8 = response.encode("utf-8").decode("utf-8")  # Явная перекодировка

            await self.send(text_data=html_data)  # Отправляем как UTF-8
        except json.JSONDecodeError:
            print("\n\n[ChatConsumer] Ошибка декодирования JSON\n\n")

    async def disconnect(self, close_code):
        print(f"\n\n[ChatConsumer] Клиент отключен: {close_code}\n\n")

