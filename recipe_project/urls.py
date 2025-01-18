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
from django.http import JsonResponse  # json형식으로 응답을 위한 도구
from accounts.views import login_view,main_view,profile_view,signup_view # html 로그인,메인,프로필,회원가입 뷰 불러오기기
from chatbot.views import chatbot_view  # html 챗봇 뷰 불러오기
from calories.views import calories_view  # html 칼로리 뷰 불러오기


def root_view(request):
    return JsonResponse({"message": "Welcome to Recipe API"}, status=500)

urlpatterns = [
    path('', root_view, name='root'),
    path('admin/', admin.site.urls),  # 장고 기본 관리자 페이지
    path('api/auth/', include('accounts.urls', namespace='accounts')),  # 인증 관련 urls
    path('api/food/', include('food.urls')),  # 음식 관련 urls
    path('api/chatbot/', include('chatbot.urls')),  # 챗봇 추가
    path('api/calories/', include('calories.urls')), # 칼로리 추가
    
    # JWT 관련 URL 추가
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT 발급
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT 리프레시



    #'login/' 경로로 들어오면 login_view를 실행
    path('login/', login_view, name='login'),    #'login/' 경로로 들어오면 login_view를 실행
   
    path('main/', main_view, name='main'),      # 'main/' 경로로 들어오면 main_view를 실행
   
    path('profile/', profile_view, name='profile'),  # 'profile/' 경로로 들어오면 profile_view를 실행
   
    path('signup/', signup_view, name='signup'),   # 'signup/' 경로로 들어오면 signup_view를 실행
   
    path('chatbot/', chatbot_view, name='chatbot'),  # 'chatbot/' 경로로 들어오면 chatbot_view를 실행
   
    path('calories/', calories_view, name='calories'),  # 'calories/' 경로로 들어오면 calories_view를 실행


]

