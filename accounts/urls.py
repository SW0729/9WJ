from django.urls import path
<<<<<<< HEAD
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    ProfileView,
    CustomTokenObtainPairView, #JWT 토큰 추가
    RegisterView, #JWT 토큰 갱신
    LogoutView,
    TagListView,
    UserLoginAPI,  # 로그인 API 추가
)

app_name = 'accounts'

urlpatterns = [
    # 사용자 등록(회원가입)
    path('register/', RegisterView.as_view(), name='register'),

    # 사용자 로그인(JWT 토큰 생성)
    path('login/', UserLoginAPI.as_view(), name='login'),

    # JWT 토큰 발급 (커스텀)
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # JWT 토큰 갱신
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 사용자 프로필(마이페이지) 조회
    path('profile/', ProfileView.as_view(), name='profile'),

    # 사용자 로그아웃
    path('logout/', LogoutView.as_view(), name='logout'),

    # 태그 목록 조회
    path('tags/', TagListView.as_view(), name='tag-list'),
]
=======
from .views import UserCreateView 

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),  # 사용자 등록 API
]
>>>>>>> JSH
