import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from config.consumers import GameConsumer  # GameConsumer import
from django.urls import re_path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')  # 개발 설정으로

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # WebSocket 연결이 이 URL로 오면 GameConsumer로 연결
            re_path(r"ws/game/(?P<game>\w+)/(?P<room>\w+)$", GameConsumer.as_asgi()),  # 경로 설정
        ])
    ),
})
