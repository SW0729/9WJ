from django.contrib.auth.models import AbstractUser  # Django 기본 사용자 모델을 확장
from django.db import models  # Django에서 데이터베이스 모델을 사용하려면 'models'가 필요

class CustomUser(AbstractUser):
    # 'AbstractUser'를 상속하여 기본 사용자 모델을 확장합니다.
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)  # 프로필 이미지를 추가 (선택적)
    
    # 충돌을 피하기 위해 related_name을 설정
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # 'groups' 필드에 대한 역참조 이름을 변경
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # 'user_permissions' 필드에 대한 역참조 이름을 변경
        blank=True
    )
