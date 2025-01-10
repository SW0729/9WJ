from django.urls import path
from .views import RecipeListCreateView, RecipeDetailView, RecipeSearchView

urlpatterns = [
    path('recipes/', RecipeListCreateView.as_view(), name='recipe-list-create'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipes/search/', RecipeSearchView.as_view(), name='recipe-search'),
]