import warnings  # warnings 모듈 import

# DeprecationWarning 무시
warnings.filterwarnings("ignore", category=DeprecationWarning)


from django.shortcuts import render
from rest_framework.views import APIView  # DRF에서 제공하는 기본 APIView 클래스
from rest_framework.response import Response  # 클라이언트에게 응답을 보내는 클래스
from rest_framework import status  # HTTP 상태 코드를 관리하는 클래스
from .link import chatbot_response  # link.py에서 AI 응답을 생성하는 함수를 가져옴
from .calorie_helper import calculate_calories  # 칼로리 계산 함수 호출
from .KJK_data_collect import collect_recipe_data  # 데이터 수집 함수 호출

class ChatBotAPIView(APIView):
    """
    사용자가 입력한 메시지에 대해 AI가 응답을 생성하는 API

    """

    def post(self, request):
        """
        POST 요청을 처리하여 사용자 입력(message)에 대한 AI 응답
        """
        # 사용자가 보낸 데이터에서 "message" 키의 값을 가져옴
        user_input = request.data.get("message", "")

        # 만약 message가 비어 있으면 에러 응답을 보냄
        if not user_input:
            return Response(
                {"error": "메시지를 입력해주세요!"},  # 사용자에게 메시지를 입력하라고 알려줌
                status=status.HTTP_400_BAD_REQUEST  # HTTP 상태 코드 400: 잘못된 요청
            )

        # AI 챗봇 응답 생성 (link.py의 chatbot_response 함수 사용)
        response = chatbot_response(user_input)

        # 생성된 응답을 클라이언트에게 보냄
        return Response(
            {"response": response},  # AI가 생성한 답변을 JSON 형태로 반환
            status=status.HTTP_200_OK  # HTTP 상태 코드 200: 성공
        )