from django.db import models

# 칼로리 계산기 함수부분 
#     time = '아침'
#     response = input('아침으로는 무엇을 드셨나요?: ')
#     food_time = input('혹시 아침은 몇시에 드셨나요?: ')
#     age = input('현재 나이가 어떻게 되시죠?: ')
#     is_on_diet = input('현재 다이어트 중이신가요?: ')
#     completion = client.chat.completions.create(

# p 27~31
#===========================================================

class calories(models.model):
    age = models.IntegerField(verbose_name="나이") 
    # 유저 나이 저장
    food_time = models.CharField(max_length=15, verbose_name="식사 시간") 
    #삼식세끼 중 한개 고르기
    food_details = models.TextField(verbose_name="음식 정보") 
    # 유저가 먹은 음식 정보 프롬프트가 너무 길었어 길게 저장
    is_on_diet = models.BooleanField(default=False, verbose_name="다이어트 중") 
    # 유저가 다이어트중인가? 거짓말
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 날짜") 
    # 편의기능 저장한 시간을 자동 기록기능
