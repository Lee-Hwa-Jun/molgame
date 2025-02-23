from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.shortcuts import render  # render 함수 import 추가

urlpatterns = [
                  # 방 선택 화면 (omok_main.html)
                  path('', lambda request: render(request, 'omok_main.html'), name='main'),

                  # 게임 화면 (omok_game.html)
                  path('game/', lambda request: render(request, 'omok_game.html'), name='game'),
              ] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])