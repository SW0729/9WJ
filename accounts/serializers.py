from rest_framework import serializers
from .models import CustomUser
from food.models import Recipe, Tag  # food.models에서 Recipe와 Tag 가져오기
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# 사용자 시리얼라이저
class CustomUserSerializer(serializers.ModelSerializer):
    """
    사용자 정보를 직렬화 및 사용자 생성.
    """
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        새로운 사용자 생성.
        """
        user = CustomUser.objects.create_user(**validated_data)
        return user


# JWT 커스텀 토큰 시리얼라이저
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    JWT 토큰에 사용자 정보를 포함.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token


# 레시피 시리얼라이저
class RecipeSerializer(serializers.ModelSerializer):
    """
    레시피 정보를 직렬화.
    """
    tags = serializers.StringRelatedField(many=True, read_only=True)  # 태그를 문자열로 직렬화
    author = serializers.StringRelatedField(read_only=True)  # 작성자를 문자열로 직렬화

    class Meta:
        model = Recipe
        fields = '__all__'


# 태그 시리얼라이저
class TagSerializer(serializers.ModelSerializer):
    """
    태그 정보를 직렬화.
    """
    recipes = RecipeSerializer(many=True, read_only=True)  # 태그에 연결된 레시피를 포함

    class Meta:
        model = Tag
        fields = '__all__'


# 사용자 프로필 시리얼라이저
class UserProfileSerializer(serializers.ModelSerializer):
    """
    사용자 프로필과 관련된 저장된 레시피 정보를 반환.
    """
    my_recipes = serializers.SerializerMethodField()  # 사용자 레시피 필드 추가

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'my_recipes')

    def get_my_recipes(self, obj):
        """
        사용자가 작성한 레시피를 반환.
        """
        recipes = Recipe.objects.filter(author=obj)  # 현재 사용자의 레시피만 가져오기
        return RecipeSerializer(recipes, many=True).data
