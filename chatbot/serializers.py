from rest_framework import serializers
from .models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    """
    Recipe 모델 데이터를 JSON 형식으로 변환
    """
    class Meta:
        model = Recipe
        fields = '__all__'  # 모든 필드를 포함