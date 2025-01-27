from rest_framework import serializers
from .models import ingredients
import markdown

class IngredientSerializer(serializers.ModelSerializer):
    ingredients = serializers.CharField()
    language = serializers.CharField()
    class Meta:
        model = ingredients
        fields = '__all__'  # 모든 필드를 포함

        
    def to_representation(self, instance):
        # 기본적으로 직렬화된 데이터 가져오기
        data = super().to_representation(instance)
        
        # 마크다운을 HTML로 변환
        if 'content' in data:
            data['content'] = markdown.markdown(data['content'])
        return data