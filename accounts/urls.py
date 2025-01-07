from django.urls import path
from .views import ProfileView
from .views import CustomTokenObtainPairView, LogoutView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),  # 사용자 프로필 API
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # 로그인
    path('logout/', LogoutView.as_view(), name='logout'),  # 로그아웃
 ]