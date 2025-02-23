import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from config.consumers import GameConsumer, LobbyConsumer  # config/consumers.py에서 가져옴

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(r"ws/game/(?P<game>\w+)/(?P<room>\w+)$", GameConsumer.as_asgi()),
            re_path(r"ws/game/omok/lobby$", LobbyConsumer.as_asgi()),
        ])
    ),
})