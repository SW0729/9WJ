<<<<<<< HEAD
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Recipe, FavoriteRecipe, Tag
from .serializers import RecipeSerializer, RecipeCreateSerializer, FavoriteRecipeSerializer


class RecipeListCreateView(generics.ListCreateAPIView):
    """
    레시피 목록 조회 및 생성 API
    """
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        GET 요청에서는 RecipeSerializer를, POST 요청에서는 RecipeCreateSerializer를 사용
        """
        if self.request.method == 'POST':
            return RecipeCreateSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        """
        레시피를 저장할 때 작성자를 현재 사용자로 설정
        """
        serializer.save(author=self.request.user)


class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    특정 레시피 조회, 수정, 삭제 API
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """
        수정 시 작성자를 현재 사용자로 유지
        """
        serializer.save(author=self.request.user)


class FavoriteRecipeView(generics.CreateAPIView):
    """
    레시피 즐겨찾기 추가/삭제 API
    """
    serializer_class = FavoriteRecipeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        즐겨찾기 추가 또는 삭제
        """
        recipe_id = request.data.get('recipe_id')
        if not recipe_id:
            return Response({"error": "레시피 ID가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            return Response({"error": "레시피를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        favorite, created = FavoriteRecipe.objects.get_or_create(user=request.user, recipe=recipe)
        if not created:
            # 이미 즐겨찾기에 추가된 경우 삭제
            favorite.delete()
            return Response({"message": "즐겨찾기에서 삭제되었습니다."}, status=status.HTTP_200_OK)

        return Response({"message": "즐겨찾기에 추가되었습니다."}, status=status.HTTP_201_CREATED)


class UserFavoriteListView(generics.ListAPIView):
    """
    사용자가 즐겨찾기한 레시피 목록 조회 API
    """
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        현재 사용자가 즐겨찾기한 레시피만 반환
        """
        return Recipe.objects.filter(favoriterecipe__user=self.request.user)
=======
from rest_framework import generics  # DRF에서 제공하는 제네릭 뷰 사용
from rest_framework.permissions import IsAuthenticated  # 인증된 사용자만 접근할 수 있게 설정
from .models import Recipe  # 'Recipe' 모델을 사용
from .serializers import RecipeSerializer  # 'RecipeSerializer'를 사용

class RecipeListCreateView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()  # 모든 레시피를 가져오기기
    serializer_class = RecipeSerializer  
    permission_classes = [IsAuthenticated]  # 인증을 거친  사용자만 사용가능

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # 레시피를 저장할 때, 작성자를 현재 사용자로 설정
>>>>>>> JSH
