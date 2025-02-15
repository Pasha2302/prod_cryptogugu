from django.urls import re_path
from app.ws.ws_conn.consumers import ChatConsumer, CoinCheckConsumer


websocket_urlpatterns = [
    re_path(r'ws/check-coin-name/$', CoinCheckConsumer.as_asgi()),

    re_path(r"ws/chat/$", ChatConsumer.as_asgi()),
]
