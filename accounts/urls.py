from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    ProfileView,
    CustomTokenObtainPairView,
    RegisterView,
    LogoutView,
    TagListView,  # 올바른 뷰 이름으로 교체
)

app_name = 'accounts'


urlpatterns = [
    # 사용자 등록(회원가입)
    path('register/', RegisterView.as_view(), name='register'),

    # 사용자 로그인(JWT 토큰 생성)
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # JWT 토큰 갱신
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 사용자 프로필(마이페이지) 조회
    path('profile/', ProfileView.as_view(), name='profile'),

    # 사용자 로그아웃
    path('logout/', LogoutView.as_view(), name='logout'),
    # 태그 목록
    path('tags/', TagListView.as_view(), name='tag-list'),  


    # 'login/' 경로로 들어오면 login_view를 실행
    path('login/', views.login_view, name='login'),  
    # 'main/' 경로로 들어오면 main_view를 실행
    path('main/', views.main_view, name='main'),     
    # 'profile/' 경로로 들어오면 profile_view를 실행
    path('profile/', views.profile_view, name='profile'), 
    # 'signup/' 경로로 들어오면 signup_view를 실행
    path('signup/', views.signup_view, name='signup'),  
]