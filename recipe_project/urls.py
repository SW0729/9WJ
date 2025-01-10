"""
URL configuration for recipe_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  # include는 다른 URL을 포함시킬 때 사용
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # JWT 관련 뷰
from django.http import JsonResponse  # JsonResponse를 가져오기

def root_view(request):
    return JsonResponse({"message": "Welcome to Recipe API"}, status=500)

urlpatterns = [
    path('', root_view, name='root'),
    path('admin/', admin.site.urls),  # 장고 기본 관리자 페이지
    path('api/auth/', include('accounts.urls', namespace='accounts')),  # 인증 관련 urls
    path('api/food/', include('food.urls')),  # 음식 관련 urls
    path('api/chatbot/', include('chatbot.urls')),  # 챗봇 추가
    
    
    # JWT 관련 URL 추가
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT 발급
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT 리프레시
]

