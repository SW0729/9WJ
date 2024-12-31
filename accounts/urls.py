from django.urls import path
from .views import UserCreateView 

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),  # 사용자 등록 API
]
