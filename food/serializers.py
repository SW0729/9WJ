from rest_framework import serializers
from .models import Recipe, Tag, FavoriteRecipe # 레시피,태그.즐겨찾기 모델 가져오기 (즐겨찾기는 일딴 넣어놈)


class TagSerializer(serializers.ModelSerializer):
    """
    태그 정보를 직렬화, 여러 태그들을 관리리
    """
    class Meta:
        model = Tag
        fields = ['id', 'name']


class RecipeSerializer(serializers.ModelSerializer):
    """
    레시피 정보를 직렬화 및 생성 시 태그 데이터를 처리 
    """
    tags = serializers.ListField(
        child=serializers.CharField(max_length=100),  # 태그는 문자열 리스트로 받음
        write_only=True,  # 생성할 때만 사용, 응답에는 포함되지 않음
    )
    author = serializers.StringRelatedField()  # 작성자의 이름만 표시

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'category', 'ingredients', 'steps', 'tags', 'author']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])  # 태그 데이터 가져오기
        recipe = Recipe.objects.create(**validated_data)  # 레시피 생성
        for tag_name in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_name)  # 태그가 없으면 새로 생성
            recipe.tags.add(tag)  # 태그와 레시피 연결
        return recipe

class RecipeCreateSerializer(serializers.ModelSerializer):
    """
    레시피 생성 시 사용되는 시리얼라이저클래스 지정정
    """
    tags = serializers.ListField(
        child=serializers.CharField(max_length=100),
        write_only=True,  # 태그는 쓰기 전용
    )

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'category', 'ingredients', 'steps', 'tags', 'author']

    def create(self, validated_data):# 새 레시피와 태그를 db에 저장하는 함수
        tags_data = validated_data.pop('tags', []) # 태그 데이터 가져오기
        recipe = Recipe.objects.create(**validated_data) # 레시피 생성
        for tag_name in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_name)# 태그생성, 기존 태그가 없으면 새로 생성기능 추가가
            recipe.tags.add(tag) # 레시피와 태그를 연결
        return recipe


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """
    즐겨찾기 레시피를 직렬화
    """
    class Meta:
        model = FavoriteRecipe 
        fields = ['id', 'user', 'recipe', 'favorited_at'] # 즐겨찾기 기능 포함