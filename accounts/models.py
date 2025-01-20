from django.contrib.auth.models import AbstractUser #django에서 제공하는 사용자 모델
from django.db import models # db 모델 만들기 위한 모듈


class CustomUser(AbstractUser):
 

    # username을 아예 제거하여 email만 사용
    username = None  # username 필드를 제거

    # email을 필수로 설정
    email = models.EmailField(unique=True)


    groups = models.ManyToManyField(
        'auth.Group',# 계정을 사용한  사용자가 그룹을 애기함
        related_name='customuser_set',  # 고유한 이름으로 변경
        blank=True # 그룹을 비워도 ok
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', #권한 세이브
        related_name='customuser_permissions_set',  # 고유한 이름으로 변경
        blank=True # 그룹을 비워도 ok
    )

    def get_my_recipes(self):
        """
        사용자가 작성한 레시피를 목록을 가져오는 함수수
        """
        from food.models import Recipe # 레시피 모델 임포트
        return Recipe.objects.filter(author=self)  # 현재 사용자가 작성한 레시피만 가져오기기


class Recipe(models.Model):
    """
    레시피 클래스는 요리 레시피를 정보를 저장하기
    """
    title = models.CharField(max_length=255) # 레시피 제목
    description = models.TextField()# 레시피 설명
    ingredients = models.TextField()# 래사파 재료
    instructions = models.TextField()# 요리 만드는법
    created_at = models.DateTimeField(auto_now_add=True)# 시간대 저장
    updated_at = models.DateTimeField(auto_now=True)# 수정 시간대 저장
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="recipes")
    # 유저 모델 가져오기 , 사용자가 삭제하면 레시피도 삭제 , 레시피 목록을 가져오기 위한 이름 부여
    def __str__(self):
        return self.title


class Tag(models.Model):
    """
    태그 클래스를 지정하여 레시피에 추가 할 수 있게 태그 정보를 저장한다
    """
    name = models.CharField(max_length=50, unique=True) # 태그 이름 지정
    recipes = models.ManyToManyField(Recipe, related_name="tags") # 태그와 연결된 레시피 목록 이름지정

    def __str__(self):
        return self.name

    
