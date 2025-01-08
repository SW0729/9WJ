from django.db import models
from accounts.models import CustomUser  # 사용자 모델 가져오기

class RecipeCategory(models.TextChoices):
    """
    레시피 카테고리를 정의하는 클래스.
    양식, 중식, 일식, 한식으로 나누기기
    """
    WESTERN = '양식', '양식'
    JAPANESE = '일식', '일식'
    KOREAN = '한식', '한식'
    CHINESE = '중식', '중식'

class Tag(models.Model):
    """
    레시피 태그를 저장하는 모델.
    """
    name = models.CharField(max_length=100, unique=True)  # 태그 이름

    def __str__(self):
        return self.name

class Recipe(models.Model):
    """
    레시피 정보를 저장하는 모델.
    """
    title = models.CharField(max_length=200)  # 레시피 제목
    description = models.TextField()  # 레시피 설명
    category = models.CharField(
        max_length=10,
        choices=RecipeCategory.choices,  # 카테고리 선택
        default=RecipeCategory.WESTERN,  # 기본값
    )
    ingredients = models.TextField()  # 재료 목록
    steps = models.TextField()  # 조리 과정
    tags = models.ManyToManyField(Tag, blank=True)  # 태그
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # 작성자

    def __str__(self):
        return self.title
