from django.db import models
from accounts.models import CustomUser  # 사용자 모델 가져오기


class RecipeCategory(models.TextChoices):
    """
    레시피 카테고리 정의를 해주기
    """
    WESTERN = '양식', '양식'
    JAPANESE = '일식', '일식'
    KOREAN = '한식', '한식'
    CHINESE = '중식', '중식'


class Tag(models.Model):
    """
    레시피에 사용할 태그를 저장
    """
    name = models.CharField(max_length=100, unique=True)  # 태그 이름을 저장

    class Meta:
        verbose_name = "태그" # 관리자 페이지에 이름 지정
        verbose_name_plural = "태그들"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    레시피 정보를 저장장
    """
    title = models.CharField(max_length=200)  # 제목
    description = models.TextField(blank=True, null=True)  # 설명 - 필수 아닌거거
    category = models.CharField(
        max_length=10,
        choices=RecipeCategory.choices,  # 카테고리 선택
        default=RecipeCategory.WESTERN,  # 기본값 - 양식을 임시 지정
    )
    ingredients = models.TextField()  # 재료 목록
    steps = models.TextField()  # 조리 과정
    tags = models.ManyToManyField(Tag, blank=True, related_name="food_recipes")  # 태그 연결 - 여러 태그연결가능
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="food_recipes")  # 작성자
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시각
    updated_at = models.DateTimeField(auto_now=True)  # 수정 시각

    class Meta:
        verbose_name = "레시피" # 관리자 웹에서 표시 이름 지정정
        verbose_name_plural = "레시피들" # 복수형을 지정하라고 해야 오류가 없다고 머시라고함
        ordering = ['-created_at']  # 최신 레시피 먼저 정렬

    def __str__(self):
        return self.title

# 추가적인 기능 찾다가 즐겨찾기도 넣어봄
class FavoriteRecipe(models.Model):
    """
    사용자가 즐겨찾기한 레시피
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="favorites")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="favorited_by")
    favorited_at = models.DateTimeField(auto_now_add=True)  # 즐겨찾기 추가 시간

    class Meta:
        verbose_name = "즐겨찾기 레시피"
        verbose_name_plural = "즐겨찾기 레시피들"
        unique_together = ('user', 'recipe')  # 동일한 사용자와 레시피 중복 즐겨찾기 금지

    def __str__(self):
        return f"{self.user.username} - {self.recipe.title}" 
    # 출력형식을 사용자이름과 레시피 제목으로 일딴 지정정