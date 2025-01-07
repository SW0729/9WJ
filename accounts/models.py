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
        사용자가 작성한 레시피만 반환하는 함수
        """
        from food.models import Recipe
        return Recipe.objects.filter(author=self)  # 작성한 레시피만 반

    
