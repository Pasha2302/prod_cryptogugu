import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string

# daphne -b 0.0.0.0 -p 8005 src.asgi:application


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


class CoinCheckConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        print(f"\n\n[DEBUG CoinCheckConsumer (61)] RAW text_data: {text_data}\n\n")
        data = json.loads(text_data)
        coin_name = data.get('post_title', '').strip()
        from app.models_db.coin import Coin

        # Асинхронная проверка в базе данных через sync_to_async
        coin_exists = await sync_to_async(Coin.objects.filter(name__iexact=coin_name).exists)()
        print(f"[DEBUG CoinCheckConsumer (67)] coin_exists: {coin_exists}")

        # Рендеринг шаблона в отдельном синхронном потоке
        html_data = render_to_string(
            template_name='app/components_html/coins/add/coin_check.html',
            context={'check_coin': coin_exists}
        )

        # Отправка данных обратно
        await self.send(text_data=html_data)


