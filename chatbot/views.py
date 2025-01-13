from django.shortcuts import render # 템플릿 함수수
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Recipe
from .serializers import RecipeSerializer
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from rest_framework import serializers
from .KJK_data_collect import recipe_finder  #  kJK_data_collect 바로 연결하고 함수 불러오기기
import os
import openai
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY2")

# 챗봇 페이지
def chatbot_view(request):
    return render(request, 'chatbot.html') # 'chatbot' 랜더링



# 요청 데이터를 확인하기 위한 클래스
class RecipeSearchSerializer(serializers.Serializer):
    # 검색어 (필수)
    query = serializers.CharField(required=True, max_length=200)
    # 요리 종류 (필수) - 선택 가능한 값만 사용 가능
    country_food = serializers.ChoiceField(choices=["korean", "japanese", "western", "chinese"], required=True)


# 모든 레시피를 가져오거나 새 레시피를 만드는 API
class RecipeListCreateView(ListCreateAPIView):
    """
    요리 데이터를 조회하거나 새 데이터를 생성하는 API
    """
    queryset = Recipe.objects.all()  # 데이터베이스에 있는 모든 레시피 가져오기
    serializer_class = RecipeSerializer  # 데이터를 JSON 형식으로 변환하거나 읽기


# 특정 레시피를 조회, 수정, 삭제하는 API
class RecipeDetailView(RetrieveUpdateDestroyAPIView):
    """
    특정 요리 데이터를 조회, 수정, 삭제하는 API
    """
    queryset = Recipe.objects.all()  # 데이터베이스에서 레시피 가져오기
    serializer_class = RecipeSerializer  # 데이터를 JSON 형식으로 변환하거나 읽기


# Chroma 검색을 이용한 요리 검색 API
class RecipeSearchView(APIView):
    """
    검색어와 요리 종류를 이용해 레시피를 검색하는 API
    """
    def post(self, request):
        # 요청 데이터 확인
        serializer = RecipeSearchSerializer(data=request.data)
        if not serializer.is_valid():  # 데이터가 잘못된 경우
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 검색어와 요리 종류 가져오기
        query = serializer.validated_data['query']
        country_food  = serializer.validated_data['country_food']

        try:
            # `recipe_finder`를 호출하여 결과 얻기
            results = recipe_finder(query, country_food)

            # 검색 결과가 없을 경우 처리
            if not results:
                return Response({"message": "검색 결과가 없습니다. 다른 키워드로 시도해보세요."}, status=status.HTTP_200_OK)

            # 성공적으로 결과 반환
            return Response({"results": results}, status=status.HTTP_200_OK)

        except ValueError as ve:
            # 잘못된 값 처리
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # 기타 예외 처리
            return Response({"error": f"서버 오류: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)