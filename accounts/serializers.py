from rest_framework import serializers # 직렬화 도구 가져오기
from .models import CustomUser# 사용자 모델 가져오기
from food.models import Recipe, Tag# food.models에서 Recipe와 Tag 가져오기
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer# jwt
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


# 사용자 시리얼라이저
class CustomUserSerializer(serializers.ModelSerializer):
    """
    사용자 정보를 직렬화하거나 새로운 사용자를 생성
    """
    class Meta:
        model = CustomUser # 사용할 데이터 모델 설정
        fields = ('id', 'email', 'password') # 필드 설정 #usersname 제외외
        extra_kwargs = {'password': {'write_only': True}} # 비밀번호를 쓰기
        exclude = ["username"]

    def create(self, validated_data):
        """
        새로운 사용자 생성 매서드
        """
        user = CustomUser.objects.create_user(**validated_data)# 오브젝유저에 사용자 생성할 정의
        return user


# JWT 커스텀 토큰 시리얼라이저
class CustomTokenObtainPairSerializer(serializers.Serializer):
    """
    이메일과 비밀번호를 사용하여 JWT 토큰을 발급하는 시리얼라이저
    """
    email = serializers.EmailField()  # 이메일 필드
    password = serializers.CharField(write_only=True)  # 비밀번호 필드
    # username = serializers.CharField(required=False)

    # 시리얼라이저가 클라이언트로부터 받은 데이터를 처리하는 부분
    def validate(self, attrs):
        # 이메일과 비밀번호를 클라이언트 요청에서 가져옴
        email = attrs.get('email')  # 유저 이메일일
        password = attrs.get('password')  # 유저 비밀번호


       

        # 이메일로 사용자 찾기
        try:
            user = CustomUser.objects.get(email=email)  # 이메일로 사용자 검색
        except CustomUser.DoesNotExist:
            # 이메일이 틀리면 에러 메시지 반환
            raise serializers.ValidationError({"error": "존재하지 않는 이메일입니다."})

        # 비밀번호 확인
        if not user.check_password(password):  # 비밀번호가 틀리면
            raise serializers.ValidationError({"error": "비밀번호가 틀렸습니다."})

        # 사용자 인증이 성공하면 JWT 토큰 생성
        refresh = RefreshToken.for_user(user)  # 리프레시 토큰 생성

        # 토큰과 사용자 정보를 반환
        return {
            'refresh': str(refresh),  # 리프레시 토큰을 문자열로 변환
            'access': str(refresh.access_token),  # 액세스 토큰을 문자열로 변환
            # 'username': user.username,  # 사용자 이름
            'email': user.email,  # 사용자 이메일
        }

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
