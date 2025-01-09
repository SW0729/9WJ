from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser, Recipe, Tag
from .serializers import (
    CustomUserSerializer,
    RecipeSerializer,
    TagSerializer,
    CustomTokenObtainPairSerializer,
)

# 회원가입
class RegisterView(APIView):
    """
    회원가입 API
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 로그인 (JWT)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# 로그아웃
class LogoutView(APIView):
    """
    로그아웃 API
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "로그아웃 완료"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# 마이페이지 (사용자 정보 + 레시피 저장)
class ProfileView(APIView):
    """
    사용자 프로필 및 저장된 레시피 관리 API
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def post(self, request):
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 레시피 목록 및 생성
class RecipeListCreateView(ListCreateAPIView):
    """
    레시피 목록 보기 및 새로운 레시피 생성 API
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


# 특정 레시피 조회, 수정, 삭제
class RecipeDetailView(RetrieveUpdateDestroyAPIView):
    """
    특정 레시피 조회, 수정, 삭제 API
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]


# 태그 목록 보기 및 생성
class TagListView(ListCreateAPIView):
    """
    태그 목록 보기 및 새로운 태그 생성 API
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer