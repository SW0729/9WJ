from rest_framework import serializers #시리어라이즈 사용위해 임포트
from .models import Recipe, Ingredient # 'recipe', 'ingredient' 모델 불러오기


class Ingredientserializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient # 'ingredient' 모델 사용
        fields = ['id', 'name', 'desceription'] # 보여줄 필드를 설정


class RecipeSerializer(serializers.ModelSerializer):
    Ingredient = Ingredientserializer(many=True) # 여러 개의 재료를 사용한다는걸 정의 , 여러 개의 재료를 처리를 한다다
     

    class Meta:
       model = Recipe # recipe 모델사용
       flelds = ['id', 'title', 'description', 'ingredients', 'steps', 'author'] # 필드 설정정