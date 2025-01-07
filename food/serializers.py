from rest_framework import serializers
from .models import Recipe, Tag

class TagSerializer(serializers.ModelSerializer):
    """
    태그 정보를 직렬화.
    """
    class Meta:
        model = Tag
        fields = ['id', 'name']

class RecipeSerializer(serializers.ModelSerializer):
    """
    레시피 정보를 직렬화.
    """
    tags = TagSerializer(many=True, read_only=True)  # 태그를 읽기 전용으로 포함

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'category', 'ingredients', 'steps', 'tags', 'author']