from django.urls import path

from hooks_tg.views import HookBotView

urlpatterns = [
    path('', HookBotView.as_view(), name='hook_tg'),
]