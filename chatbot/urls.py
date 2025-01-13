from django.urls import path
from .views import RecipeListCreateView, RecipeDetailView, RecipeSearchView
from . import views

urlpatterns = [
    path('recipes/', RecipeListCreateView.as_view(), name='recipe-list-create'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipes/search/', RecipeSearchView.as_view(), name='recipe-search'),

    path('chatbot/', views.chatbot_view, name='chatbot'), # '/chat/' 경로로 들어오면 chat_view를 실행
]