from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    사용자 모델(CustomUser)
    Django의 기본 사용자 모델(AbstractUser)을 확장
    """

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # 고유한 이름으로 변경
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',  # 고유한 이름으로 변경
        blank=True
    )

    def get_my_recipes(self):
        """
        사용자가 작성한 레시피를 반환.
        """
        from food.models import Recipe
        return Recipe.objects.filter(author=self)  # 현재 사용자가 작성한 레시피만 반환


class Recipe(models.Model):
    """
    레시피 모델
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="recipes")

    def __str__(self):
        return self.title


class Tag(models.Model):
    """
    태그 모델
    """
    name = models.CharField(max_length=50, unique=True)
    recipes = models.ManyToManyField(Recipe, related_name="tags")

    def __str__(self):
        return self.name

    
