from django.urls import path
<<<<<<< HEAD
from .views import (
    RecipeListCreateView,
    RecipeDetailView,
    FavoriteRecipeView,
    UserFavoriteListView
)

urlpatterns = [
    path('', RecipeListCreateView.as_view(), name='recipe-list-create'),  # 레시피 목록 조회 및 생성 API
    path('<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),  # 특정 레시피 조회, 수정, 삭제 API
    path('favorites/', FavoriteRecipeView.as_view(), name='favorite-recipe'),  # 레시피 즐겨찾기 API
    path('favorites/my/', UserFavoriteListView.as_view(), name='user-favorites'),  # 사용자 즐겨찾기 목록 API
]
=======
from .views import RecipeListCreateView# 새로운 레시피를 생성 기능 설정정

urlpatterns = [
    path('', RecipeListCreateView.as_view(), name='recipe-list-create'),  # 레시피 목록 조회 및 생성 API
]

# '': 기본 url 설정 기본경로를 지정
# name = 'recipe-list-create' url 이름 설정 레시피리스트 이름으로 설정 사용할 수 있게함
>>>>>>> JSH
