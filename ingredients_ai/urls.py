from django.urls import path
from .views import IngredientSearchView

urlpatterns = [
    path('ingredients/search/', IngredientSearchView.as_view(), name='ingredients'),
]