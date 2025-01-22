from django.urls import path
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
