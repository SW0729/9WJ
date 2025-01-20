from rest_framework import serializers
from .models import calories

class Caloriesserializer(serializers.ModelSerializer): # 칼로리 모델 직렬화하기기
    class Meta:
        model = calories # 칼로리 모델 지정
        fields = '__all__'  # 모델에 지정한 데이터들 전부 저장


    def validate_age(self, value):
        if value < 0:
            raise serializers.ValidationError("나이는 0 이상의 값이어야 합니다.")
        return value

    def validate_food_time(self, value):
        allowed_values = ['아침', '점심', '저녁']
        if value not in allowed_values:
            raise serializers.ValidationError(f"'{value}'는 올바른 식사 시간이 아닙니다.")
        return value