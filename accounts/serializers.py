from rest_framework import serializers
from .models import CustomUser
from food.models import Recipe  # 사용자 저장된 레시피를 직렬화하기 위해 가져오기

class CustomUserSerializer(serializers.ModelSerializer):
    """
    사용자 정보를 직렬화.
    """
    my_recipes = serializers.SerializerMethodField()  # 사용자의 저장된 레시피 추가

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'my_recipes']  # 반환할 필드

    def get_my_recipes(self, obj):
        """
        사용자가 작성한 레시피를 반환.
        """
        from food.serializers import RecipeSerializer
        recipes = Recipe.objects.filter(author=obj)  # 현재 사용자의 레시피만 가져오기
        return RecipeSerializer(recipes, many=True).data
