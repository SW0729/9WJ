from django.db import models

class Recipe(models.Model):
    country_food = models.CharField(max_length=20)  # 요리 종류 (한식, 양식 등)
    content = models.TextField()  # 레시피 내용

    def __str__(self):
        return f"{self.food_type}: {self.content[:20]}"
