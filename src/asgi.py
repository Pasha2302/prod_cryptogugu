import os
import django  # Добавляем импорт Django

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

from app.ws.ws_routes.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

django.setup()  # Гарантируем инициализацию приложений

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Обычные Django Views
    "websocket": URLRouter(websocket_urlpatterns),  # WebSocket через Channels
})
