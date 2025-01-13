from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Recipe
from .serializers import RecipeSerializer
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from rest_framework import serializers
import os
import openai
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY2")

# 요청 데이터를 확인하기 위한 클래스
class RecipeSearchSerializer(serializers.Serializer):
    # 검색어 (필수)
    query = serializers.CharField(required=True, max_length=200)
    # 요리 종류 (필수) - 선택 가능한 값만 사용 가능
    food_type = serializers.ChoiceField(choices=["korean", "japanese", "western", "chinese"], required=True)


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
        food_type = serializer.validated_data['food_type']

        # Chroma 데이터베이스 경로 설정
        persist_directory = os.path.join(os.path.dirname(__file__), f"chroma_{food_type.lower()}")

        # 데이터베이스가 없으면 에러 반환
        if not os.path.exists(persist_directory):
            return Response({"error": f"{food_type}에 대한 데이터베이스를 찾을 수 없습니다. 디렉토리를 확인하세요: {persist_directory}"}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Chroma와 OpenAI를 사용해 데이터 검색 준비
            embeddings = OpenAIEmbeddings()  # 검색할 데이터의 의미를 이해하는 도구
            vector_store = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
            results = vector_store.as_retriever().get_relevant_documents(query)  # 검색어와 맞는 데이터 찾기
        except Exception as e:
            # 예기치 못한 오류 처리
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 검색 결과가 없으면 메시지 반환
        if not results:
            return Response({"message": "검색 결과가 없습니다. 다른 키워드로 시도해보세요."}, status=status.HTTP_200_OK)

        # 검색 결과 반환
        return Response({"results": [doc.page_content for doc in results]})