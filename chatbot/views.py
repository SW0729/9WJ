from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Recipe
from .serializers import RecipeSerializer
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import os


class RecipeListCreateView(ListCreateAPIView):
    """
    요리 데이터를 조회하거나 새 데이터를 생성하는 API (CRUD)
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeDetailView(RetrieveUpdateDestroyAPIView):
    """
    특정 요리 데이터를 조회, 수정, 삭제하는 API (CRUD)
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeSearchView(APIView):
    """
    Chroma 데이터를 활용한 검색 API
    """
    def post(self, request):
        # 요청 데이터에서 쿼리와 요리 종류 추출
        query = request.data.get('query', '')
        food_type = request.data.get('food_type', '')

        if not query or not food_type:
            return Response({"error": "쿼리와 요리 종류를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        # Chroma 경로 설정
        persist_directory = os.path.join(os.path.dirname(__file__), f"chroma_{food_type}")

        if not os.path.exists(persist_directory):
            return Response({"error": f"{food_type}에 해당하는 데이터베이스가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        # Chroma 검색
        embeddings = OpenAIEmbeddings()
        vector_store = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
        results = vector_store.as_retriever().get_relevant_documents(query)

        # 검색 결과 반환
        return Response({"results": [doc.page_content for doc in results]})

