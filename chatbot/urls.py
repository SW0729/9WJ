from django.urls import path
from .views import ChatBotAPIView

urlpatterns = [
    path('', ChatBotAPIView.as_view(), name='chatbot'),  # 챗봇 API
]