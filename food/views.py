from rest_framework import generics  # DRF에서 제공하는 제네릭 뷰 사용
from rest_framework.permissions import IsAuthenticated  # 인증된 사용자만 접근할 수 있게 설정
from .models import Recipe  # 'Recipe' 모델을 사용
from .serializers import RecipeSerializer  # 'RecipeSerializer'를 사용

class RecipeListCreateView(generics.ListCreateAPIView): # 레시피 목록을 조회하거나 생성하는 API
    queryset = Recipe.objects.all()  # 모든 레시피를 가져오기기
    serializer_class = RecipeSerializer  
    permission_classes = [IsAuthenticated]  # 인증을 거친  사용자만 사용가능

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # 레시피를 저장할 때, 작성자를 현재 사용자로 설정