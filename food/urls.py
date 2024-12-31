from django.urls import path
from .views import RecipeListCreateView# 새로운 레시피를 생성 기능 설정정

urlpatterns = [
    path('', RecipeListCreateView.as_view(), name='recipe-list-create'),  # 레시피 목록 조회 및 생성 API
]

# '': 기본 url 설정 기본경로를 지정
# name = 'recipe-list-create' url 이름 설정 레시피리스트 이름으로 설정 사용할 수 있게함
