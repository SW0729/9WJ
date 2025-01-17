from rest_framework import serializers
from .models import calories

class Caloriesserializer(serializers.ModelSerializer): # 칼로리 모델 직렬화하기기
    class Meta:
        model = calories # 칼로리 모델 지정
        fields = '__all__'  # 모델에 지정한 데이터들 전부 저장