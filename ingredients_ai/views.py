from django.shortcuts import render
import markdown
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import IngredientSerializer
from .ingredients_ai import ingredients_ai  #  kJK_data_collect 바로 연결하고 함수 불러오기기
# Create your views here.
from django.http import StreamingHttpResponse
def ingredients_view(request):
    return render(request, 'ingredients.html')

class IngredientSearchView(APIView):
    def post(self, request):
        # 요청 데이터 확인
        serializer = IngredientSerializer(data=request.data)
        if not serializer.is_valid():  
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        ingredients = serializer.validated_data['ingredients']
        language  = serializer.validated_data['language']
        
        try:
            md = markdown.Markdown(extensions=["fenced_code"])
            results = ingredients_ai(ingredients, language)
            markdown_results = md.convert(results)
            if not results:
                return Response({"results": "에러 발생! 다시 시도해 주세요!"}, status=status.HTTP_200_OK)
            return Response({"results": markdown_results}, status=status.HTTP_200_OK)

        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": f"서버 오류: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
