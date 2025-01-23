from django.urls import path
from .views import CalorieView 



urlpatterns = [
    path('', CalorieView.as_view(), name='calorie_calculator'),  # 경로는 그대로
]