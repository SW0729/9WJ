from rest_framework import serializers # 직렬화 도구 가져오기
from .models import CustomUser# 사용자 모델 가져오기
from food.models import Recipe, Tag  # food.models에서 Recipe와 Tag 가져오기
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer# jwt


# 사용자 시리얼라이저
class CustomUserSerializer(serializers.ModelSerializer):
    """
    사용자 정보를 직렬화하거나 새로운 사용자를 생성
    """
    class Meta:
        model = CustomUser # 사용할 데이터 모델 설정
        fields = ('id', 'username', 'email', 'password') # 필드 설정
        extra_kwargs = {'password': {'write_only': True}} # 비밀번호를 쓰기

    def create(self, validated_data):
        """
        새로운 사용자 생성 매서드
        """
        user = CustomUser.objects.create_user(**validated_data)# 오브젝유저에 사용자 생성할 정의
        return user


# JWT 커스텀 토큰 시리얼라이저
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    이메일과 비밀번호를 사용하여 JWT 토큰 발급
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token

    def validate(self, attrs):
        # 기존 validate 메서드 호출
        data = super().validate(attrs)

        # 이메일을 기반으로 사용자 인증
        email = attrs.get('email', None)
        password = attrs.get('password', None)

        try:
            # 이메일로 사용자 객체 가져오기
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"error": "Invalid email or password"})

        # 비밀번호 확인
        if not user.check_password(password):
            raise serializers.ValidationError({"error": "Invalid email or password"})

        # 추가 데이터 반환
        data.update({
            'username': user.username,
            'email': user.email
        })
        return data

# 레시피 시리얼라이저
class RecipeSerializer(serializers.ModelSerializer):
    
    """
    레시피 정보를 직렬화
    """
    tags = serializers.StringRelatedField(many=True, read_only=True)  # 태그를 문자열로 직렬화
    author = serializers.StringRelatedField(read_only=True)  # 작성자를 문자열로 직렬화

    class Meta:
        model = Recipe # 데이터 모델 설정
        fields = '__all__' # 모든 필드 포함


# 태그 시리얼라이저
class TagSerializer(serializers.ModelSerializer):
    """
    태그 정보를 직렬화
    """
    recipes = RecipeSerializer(many=True, read_only=True)  # 태그에 연결된 레시피를 포함

    class Meta:
        model = Tag # 데이터 모델 설정
        fields = '__all__' # 모든 필드 포함


# 사용자 프로필 시리얼라이저
class UserProfileSerializer(serializers.ModelSerializer):
    """
    사용자 프로필과 관련된 저장된 레시피 정보를 가져오기
    """
    my_recipes = serializers.SerializerMethodField()  # 사용자 레시피 필드 추가

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'my_recipes')

    def get_my_recipes(self, obj):
        """
        사용자가 작성한 레시피를 가져오기기
        """
        recipes = Recipe.objects.filter(author=obj)  # 현재 사용자의 레시피만 가져오기
        return RecipeSerializer(recipes, many=True).data
