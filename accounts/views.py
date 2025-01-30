from rest_framework.views import APIView# 기본 APIView를 가져옴
from rest_framework.response import Response# 응답을 반환하기 위한 도구
from rest_framework import status# HTTP 상태 코드를 사용하기 위한 도구
from rest_framework.permissions import IsAuthenticated, AllowAny # 인증 권한을 설정하기 위한 도구
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView# CRUD 기능을 위한 제네릭 뷰
from rest_framework_simplejwt.views import TokenObtainPairView # JWT 로그인 기능 제공
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # JWT 직렬화 도구
from rest_framework_simplejwt.tokens import RefreshToken # JWT 토큰 갱신을 위한 도구
from django.contrib.auth.models import User

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

def home_view(request):
    return render(request, 'home.html') # home.html 랜더링

# 프로필 페이지
def profile_view(request):
    return render(request, 'profile.html') # profile.html 랜더링

# 회원가입 페이지
def signup_view(request):
    return render(request, 'signup.html') # signup,html 랜더링


# JWT 토큰
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    이메일과 비밀번호를 사용하여 JWT 토큰을 발급하는 시리얼라이저
    """

    serializer_class = CustomTokenObtainPairSerializer 

    
    def validate(self, attrs):
        # 클라이언트가 요청한 이메일과 비밀번호를 가져옵니다.
        email = attrs.get('email')  # 이메일
        password = attrs.get('password')  # 비밀번호

        # 이메일로 사용자를 찾습니다.
        try:
            user = CustomUser.objects.get(email=email)  # 이메일로 사용자 검색
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"error": "존재하지 않는 이메일입니다."})  # 이메일이 없으면 에러

        # 비밀번호가 맞는지 확인합니다.
        if not user.check_password(password):  # 비밀번호 확인
            raise serializers.ValidationError({"error": "비밀번호가 틀렸습니다."})  # 틀리면 에러

        # 비밀번호가 맞으면 JWT 토큰을 생성합니다.
        refresh = RefreshToken.for_user(user)  # 리프레시 토큰 생성

        return {
            'refresh': str(refresh),  # 리프레시 토큰
            'access': str(refresh.access_token),  # 액세스 토큰
            # 'username': user.username,  # 사용자 이름
            'email': user.email,  # 사용자 이메일
        }

# 로그인 
class UserLoginAPI(APIView):
    """
    이메일과 비밀번호를 사용한 로그인 API
    """
    def post(self, request):
        # 클라이언트가 보낸 이메일과 비밀번호 가져오기
        email = request.data.get('email')  # 이메일 입력값
        password = request.data.get('password')  # 비밀번호 입력값

        # 이메일과 비밀번호가 입력되지 않았을 때 에러 반환
        if not email or not password:
            return Response(
                {"message": "이메일과 비밀번호를 입력해주세요."},  # 안내 메시지
                status=status.HTTP_400_BAD_REQUEST  # HTTP 상태코드 400: 잘못된 요청
            )

        # CustomTokenObtainPairSerializer를 사용해 데이터 검증
        serializer = CustomTokenObtainPairSerializer(data=request.data)

        # 이메일과 비밀번호가 맞는지 검증
        if serializer.is_valid():  # 데이터가 유효하면
            return Response(
                {
                    "message": "로그인 성공",  # 성공 메시지
                    "data": serializer.validated_data  # 유효한 데이터 반환 (토큰 및 사용자 정보)
                },
                status=status.HTTP_200_OK  # HTTP 상태코드 200: 성공
            )
        else:
            # 이메일 또는 비밀번호가 틀렸을 때 에러 반환
            return Response(
                {
                    "message": "로그인 실패",  # 실패 메시지
                    "errors": serializer.errors  # 에러 내용 반환
                },
                status=status.HTTP_400_BAD_REQUEST  # HTTP 상태코드 400: 잘못된 요청
            )


# 회원가입
class RegisterView(APIView):
    """
    사용자 회원가입 뷰
    """
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')


       


        if not username or not email or not password:
            return Response(
                {"message": "모든 필드를 입력해주세요."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 사용자 생성
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        return Response(
            {"message": "회원가입 성공", "username": user.username},
            status=status.HTTP_201_CREATED
        )
           
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