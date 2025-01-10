from django.urls import path
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
]