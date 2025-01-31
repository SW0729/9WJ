from django.db import models

# Create your models here.
class ingredients(models.Model):
    ingredients = models.TextField(verbose_name="재료 정보")
    language = models.TextField(verbose_name='언어 정보')