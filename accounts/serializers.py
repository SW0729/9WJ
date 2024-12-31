from rest_framework import serializers # DRF에서 시리어라이즈를 사용하기 위해 임포트
from .models import CustomUser # 'customuser' 모델을 불러오기


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser # 커스텀유저 모델을 사용
        fields = ['id', 'username', 'email', 'profile_image'] # 보여줄 데이터 설정
        