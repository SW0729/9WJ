import markdown
from django.shortcuts import render
import openai  # AI 도구
from rest_framework.views import APIView  # API 키 도구
from rest_framework.response import Response  # 유저에게 응답 리스폰스
from rest_framework import status  # HTTP 코드 지정
from .models import calories  # db 지정한 모델 불러오기
from .serializers import Caloriesserializer # 시리얼라이즈 불러오기
from .calorie_helper import calories_calculator # AI 험수 불러오기
from langdetect import detect # 자동 언어 감지 시스템 라이브러리
import os # api 보안키 설정


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY2")


#칼로리 페이지
def calories_view(request):
    return render(request, 'calories.html')




class CalorieView(APIView): # 이제 간단하게 하자 너무 길다야
    def post(self, request):
        serializer = Caloriesserializer(data=request.data)


        if serializer.is_valid():
            data = serializer.validated_data
            detected_language = detect(data['food_details']) # 언어 자동감지
            chosen_language = data.get('chosen_language', detected_language)

            
             # 한글,영어 따로 답변 따로 처리
            if detected_language == "ko":  # 한국어 처리
                prompt = f"""
                 다음 식사를 분석해주세요:
                {data['food_time']} 시간에 먹은 {data['food_details']}입니다.
                사용자의 나이는 {str(data['age'])}세이고, 다이어트를 하고 있는 상태는 {'예' if data['is_on_diet'] else '아니오'}입니다.
                """
            else:  # 영어처리
                prompt = f"""
                 Analyze the following meal for {data['food_time']}: {data['food_details']} for a {str(data['age'])} years old. Is on diet: {'Yes' if data['is_on_diet'] else 'No'}.
                """

            try:
                md = markdown.Markdown(extensions=["fenced_code"])
                print(data['food_time'], data['food_time'], data['age'], str(data['is_on_diet']), data["breakfast_time"], data["lunch_time"])
                result = calories_calculator(
                    time=data['food_time'], 
                    # filtered_file=None,  
                    response=data['food_details'], 
                    food_time=data['food_time'], 
                    age=str(data['age']),
                    is_on_diet=str(data['is_on_diet']),
                    chosen_language=chosen_language,
                    breakfast_time =  data["breakfast_time"],
                    lunch_time = data["lunch_time"],
                )
               
                # markdown 결과 후 \n을 <br>로 변환하여 HTML로 처리
                print(result)
                markdown_results = md.convert(result).replace('\n', '<br>')

                serializer.save()  # 입력 데이터를 저장
                
                return Response(markdown_results, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"error": str(traceback.format_exc())}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)