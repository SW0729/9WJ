from rest_framework.views import APIView# 기본 APIView를 가져옴
from rest_framework.response import Response# 응답을 반환하기 위한 도구
from rest_framework import status# HTTP 상태 코드를 사용하기 위한 도구
from rest_framework.permissions import IsAuthenticated, AllowAny # 인증 권한을 설정하기 위한 도구
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView# CRUD 기능을 위한 제네릭 뷰
from rest_framework_simplejwt.views import TokenObtainPairView # JWT 로그인 기능 제공
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # JWT 직렬화 도구
from rest_framework_simplejwt.tokens import RefreshToken # JWT 토큰 갱신을 위한 도구

from .models import CustomUser, Recipe, Tag
from .serializers import ( # 직렬할 애들 가져오기
    CustomUserSerializer,
    RecipeSerializer,
    TagSerializer,
    CustomTokenObtainPairSerializer,
)

from django.shortcuts import render # 장고에서 render 함수

# 로그인 페이지
def login_view(request):
    return render(request, 'login.html')# login.html  템플릿을 렌더링 

# 메인 페이지
def main_view(request):
    return render(request, 'main.html') # main.html 랜더링

# 프로필 페이지
def profile_view(request):
    return render(request, 'profile.html') # profile.html 랜더링

# 회원가입 페이지
def signup_view(request):
    return render(request, 'signup.html') # signup,html 랜더링



# 회원가입
class RegisterView(APIView):
    """
    회원가입 API
    """
    permission_classes = [AllowAny] # 모든 유저 접근 가능

    def post(self, request): # 새로운 정보를 받아서 저장
        serializer = CustomUserSerializer(data=request.data) # 전달받은 데이터 직렬화 하기
        if serializer.is_valid(): # 데이터 오류 확인
            serializer.save() # 세이브
            return Response(serializer.data, status=status.HTTP_201_CREATED) # 성공 응답
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)# 실패 시 오류응답답


# 로그인 (JWT)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer # 유저이름과 비밀번호 jwt 토큰 발급


# 로그아웃
class LogoutView(APIView):
    """
    로그아웃 API
    """
    permission_classes = [IsAuthenticated] # 인증된 유저 접근 가능

    def post(self, request):
        try:
            refresh_token = request.data["refresh"] # 리플레쉬 토큰 발급
            token = RefreshToken(refresh_token) # 리플레쉬 생성
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
        user = request.user # 현재 로그인된 유저 가져오기
        serializer = CustomUserSerializer(user) # 사용자 정보를 직렬화
        return Response(serializer.data) # 직렬화된 데이터를 응답 가져오기기

    def post(self, request): # 유저가 새로운 레시피 저장할 수 있게 지정
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():# 데이터 확인
            serializer.save(author=request.user)# 유저레시피 저장장
            return Response(serializer.data, status=status.HTTP_201_CREATED)# 성공하면 혁명
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)# 실패하면 반역


# 레시피 목록 및 생성
class RecipeListCreateView(ListCreateAPIView):
    """
    레시피 목록 보기 및 새로운 레시피 생성 API
    """
    queryset = Recipe.objects.all() # 모든 레시피 가져오기
    serializer_class = RecipeSerializer# 시리얼라이즈 해줘


# 특정 레시피 조회, 수정, 삭제
class RecipeDetailView(RetrieveUpdateDestroyAPIView):
    """
    특정 레시피 조회, 수정, 삭제 API
    """
    queryset = Recipe.objects.all()# 모든 레시피 가져오기
    serializer_class = RecipeSerializer# 클래스화 하기
    permission_classes = [IsAuthenticated]# 인증유저 접근가능


# 태그 목록 보기 및 생성
class TagListView(ListCreateAPIView):
    """
    태그 목록 보기 및 새로운 태그 생성 API
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer