from .base import *
import os
from dotenv import load_dotenv
# .env 파일 로드
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")


CSP_DEFAULT_SRC = ("'self'",)
CSP_CONNECT_SRC = ("'self'", "ws://" + os.getenv("SERVER_IP") + ":8000")

# 기본 캐시 (환경에 따라 변경)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-memory-cache",
    }
}

# 개발용 데이터베이스 (SQLite)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# 개발용 WebSocket (메모리 사용)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}