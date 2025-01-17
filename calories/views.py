from django.shortcuts import render
import openai  # AI 도구구
from rest_framework.views import APIView  # API 키 도구구
from rest_framework.response import Response  # 유저에게 응답 리스폰스스
from rest_framework import status  # HTTP 코드 지정정
from .models import calories  # db 지정한 모델 불러오기
from .serializers import Caloriesserializer # 시리얼라이즈 불러오기
from langdetect import detect # 자동 언어 감지 시스템 라이브러리
import os # api 보안키 설정


openai.api_key = os.getenv("OPENAI_API_KEY2")


#칼로리 페이지
def calories_view(request):
    return render(request, 'calories.html')




class CalorieView(APIView): # 이제 간단하게 하자 너무 길다야
    def post(self, request):
        serializer = Caloriesserializer(data=request.data)


        if serializer.is_valid():
            data = serializer.validated_data
            detected_language = detect(data['food_details']) # 언어 자동감지
            food_time_map = {
                "breakfast": "아침",
                "lunch": "점심",
                "dinner": "저녁"
            }

            if detected_language == "ko":
                food_time = food_time_map.get(data['food_time'], data['food_time'])
                diet_status = "예" if data['is_on_diet'] else "아니오"
                prompt = f"다음 식사를 분석해주세요: {food_time} 시간에 먹은 {data['food_details']}입니다. 사용자의 나이는 {data['age']}세이고, 다이어트를 하고 있는 상태는 {diet_status}입니다."
            else:  # 영어 처리
                food_time = data['food_time']
                diet_status = "Yes" if data['is_on_diet'] else "No"
                prompt = f"Analyze the following meal for {food_time}: {data['food_details']} for a {data['age']} years old. Is on diet: {diet_status}."
            try:
                response = openai.Completion.create(
                    engine="gpt-4",  # ai 대가리 설정? "gpt4미니"
                    prompt=prompt,
                    max_tokens=150 
        # ai 답변길이 임시 지정 추후에 더 지정해야함 
        # 답변이 길었어 얼마나 설정해야 할지 모르겠음음
                )
                result = response.choices[0].text.strip()
                serializer.save()
    # 유저가 보낸 데이터 직렬화 시리얼라이즈로 저장

                return Response({"analysis": result}, status=status.HTTP_200_OK) # ai 답변
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
      # 에러 메세지 지정  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
                