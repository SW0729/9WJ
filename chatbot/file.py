from dotenv import dotenv_values

# 컴퓨터의 환경변수보다 .env 우선순위를 높게 설정
config = dotenv_values(".env")
# 설정한 변수로부터 값 추출
OPENAI_API_KEY = config.get('OPENAI_API_KEY2')
# 최신화된 key가 나옴 (.env 파일 값을 변경해보면서 확인 필수!)
print(OPENAI_API_KEY)