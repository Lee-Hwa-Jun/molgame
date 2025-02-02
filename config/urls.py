# from django.contrib import admin
from django.urls import path
from django.views import generic

# WebSocket 경로는 asgi.py에서 설정하는 게 보통이지만, 여기도 예시로 작성
urlpatterns = [
    # path('admin/', admin.site.urls),  # Admin 경로
    # path('', generic.TemplateView.as_view(template_name="index.html")),  # 기본 홈페이지

    # 웹소켓 관련 라우팅은 일반적으로 asgi.py에서 처리되므로 여기에 추가할 필요 없음
    # path('ws/game/', GameConsumer.as_asgi()),  # WebSocket은 asgi.py에서 설정
]
