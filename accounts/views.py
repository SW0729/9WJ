# accounts/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from food.models import Recipe
from food.serializers import RecipeSerializer
from .serializers import CustomUserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

class ProfileView(APIView):
    """
    사용자 프로필 및 저장된 레시피를 관리하는 API.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        사용자 정보를 반환.
        """
        user = request.user  # 현재 로그인한 사용자
        serializer = CustomUserSerializer(user)  # 사용자 직렬화
        return Response(serializer.data)

    def post(self, request):
        """
        새로운 레시피를 저장.
        """
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)  # 작성자를 현재 사용자로 설정
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    사용자 정보를 포함한 JWT 토큰 생성.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 사용자 추가 정보 포함 (필요한 정보 추가 가능)
        token['username'] = user.username
        token['email'] = user.email
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    사용자 정의 로그인 API.
    """
    serializer_class = CustomTokenObtainPairSerializer


    
class LogoutView(APIView):
 
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]  # 클라이언트에서 받은 Refresh Token
            token = RefreshToken(refresh_token)
            token.blacklist()  # Refresh Token을 블랙리스트에 추가
            return Response({"message": "로그아웃 완료"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)