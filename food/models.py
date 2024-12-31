from django.db import models # 기본 설정
from accounts.models import CustomUser # 'customUser' 모델 불러오기

class Ingredient(models.Model):
    name = models.CharField(max_length=100) # 재료 이름부여 , 최대100자이내
    description = models.TextField() # 재료 설명(텍스트부여)


    def __str__(self):
        return self.name # 함수값 설정 재료 이름을 반환(유저에게 보여줄 떄 빈환값)
    


class Recipe(models.Model):
    title = models.CharField(max_length=200) # 레시피 제목설정 , 최대 200자이내
    description = models.TextField() # 레시피에 대해 서술(설명)
    Ingredient = models.ManyToManyField(Ingredient) # 여러가지 재료를 레시피에 추가하다 'manytomanyfield'는 여러 재료가 여러 요리에 연결될 수 있게 연결시켜줌
    steps = models.TextField() # 레시피 조리 과정
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE) # 작성자는 'customUser'모델과 연결


    def __str__(self): # 글자로 기본 함수값을 지정정
        return self.title # 레시피 제목을 반환 - 유저에게 보여줄떄 반환값으로 설정정