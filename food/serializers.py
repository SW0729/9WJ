from rest_framework import serializers
from .models import Recipe, Tag, FavoriteRecipe


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
    author = serializers.StringRelatedField()  # 작성자의 이름만 표시

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'category', 'ingredients', 'steps', 'tags', 'author']


class RecipeCreateSerializer(serializers.ModelSerializer):
    """
    레시피 생성 시 사용되는 시리얼라이저.
    """
    tags = serializers.ListField(
        child=serializers.CharField(max_length=100),
        write_only=True,  # 태그는 쓰기 전용
    )

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'category', 'ingredients', 'steps', 'tags']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(**validated_data)
        for tag_name in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            recipe.tags.add(tag)
        return recipe


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """
    즐겨찾기 레시피를 직렬화.
    """
    class Meta:
        model = FavoriteRecipe
        fields = ['id', 'user', 'recipe', 'favorited_at']