from django.db import models # 장고에서 데이터베이스 모델을 사요하려면 'models'가 필요
from django.contrib.auth.models import AbstractUser # 장고에서 기본 사용자 모델을 확장시켜주는 코드


# Create your models here.
class CustomUser(AbstractUser):
    # "abstractuser"를 상속해서 기본 사용자 모델을 확장 시켜주기
    profile_image = models.imageField(upload_to='profile_images/', null=True, blank=True) 
     # 프로필 이미지를 추가 (선택적)