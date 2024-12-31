from rest_framework import permissions  # 권한을 설정하는데 사용
from rest_framework_simplejwt.tokens import RefreshToken  # JWT 토큰을 생성하는 데 사용
from rest_framework.views import APIView  # 기본 APIView 클래스 임포트
from rest_framework.response import Response  # API 응답을 보내기 위한 클래스
from .serializers import CustomUserSerializer  # CustomUserSerializer를 임포트

class UserCreateView(APIView):
    permission_classes = [permissions.AllowAny] # 누구나 회원가입하게 설정

    
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data) # 요청 데이터로 시리어라이즈 객체 생성
        if serializer.is_valid():
            user = serializer.save() # 사용자 저장
            token = RefreshToken.for_user(user) # JWT 토큰 생성
            return Response({
                'refresh': str(token), #토큰화
                'access': str(token.access_token), # 토큰화
            })
        return Response(serializer.errors, status=400) 
        # 데이터가 맞지않으면 에러 응답으로 반환값 설정정