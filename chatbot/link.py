import os  # 운영 체제와 상호작용하기 위한 모듈
import openai  # OpenAI API 모듈
from dotenv import load_dotenv  # .env 파일을 로드하기 위한 모듈

# OpenAI API 키 설정
# OpenAI의 서비스를 사용하려면 API 키가 필요
# 팀원에게 받은 OpenAI API 키를 "your_openai_api_key" 대신 입력

# .env 파일 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")  # 환경 변수에서 API 키를 가져옴


def chatbot_response(user_input):
    
    try:
        # OpenAI GPT-4 모델을 호출하여 답변을 생성
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # GPT-4미니니 모델 사용
            messages=[
                {"role": "system", "content": "당신은 요리 전문가입니다. 요리와 관련된 질문에 답해주세요."},
                {"role": "user", "content": user_input},
            ],
            max_tokens=200,  # AI가 생성할 답변의 최대 단어 수
            temperature=0.7,  # 응답의 창의성 정도 (0.7은 적당한 수준)
        )

        # AI의 응답 내용 반환
        return response['choices'][0]['message']['content'].strip()

    except openai.error.OpenAIError as e:
        # OpenAI에서 발생한 오류를 처리하고 메시지 반환
        return f"오류 발생: {str(e)}"

    except Exception as e:
        # 일반적인 오류를 처리하고 메시지 반환
        return f"오류 발생: {str(e)}"
    

    """
    사용자가 입력한 질문이나 요청에 대해 AI가 대답을 생성합니다.

    - GPT-4 모델을 사용하여 응답을 만듭니다.
    - 사용자 입력을 분석하고, 적절한 답변을 생성합니다.

    Args:
        user_input (str): 사용자가 입력한 문자열. (예: "파스타 만드는 방법 알려줘")

    Returns:
        str: AI가 생성한 답변. 오류가 발생하면 오류 메시지를 반환합니다.
    """




from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
#----------------------------------------------------------------------
import requests, json
from bs4 import BeautifulSoup
import os
import openai
from openai import OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY2")
import warnings
warnings.filterwarnings(action = 'ignore')
import subprocess
import json
#----------------------------------------------------------------------
# webdriver_options = Options()
# webdriver_options.add_argument("--headless")  
# driver_service = Service(ChromeDriverManager().install()) 
# webdriver_chrome = webdriver.Chrome(service=driver_service, options=webdriver_options)
#----------------------------------------------------------------------
from KJK_data_collect import query
#저장 함수
# def save_to_index(data, file_path='C:\\Users\\kevinkim\\Desktop\\recipes\\index.json'):
#     if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
#         print("File does not exist or is empty. Initializing with an empty list.")
#         index_data = []
#     else:
#         with open(file_path, 'r', encoding='utf-8') as file:
#             try:
#                 index_data = json.load(file)
#                 if not isinstance(index_data, list):
#                     raise ValueError("Existing data is not a list. Please check the file format.")
#                 print("Existing data loaded:", index_data)
#             except json.JSONDecodeError:
#                 print("File is empty or corrupt. Initializing with an empty list.")
#                 index_data = []  
#             except ValueError as e:
#                 print(f"Error: {e}")
#                 return  

#     print("Adding new data:", data)
#     index_data.append(data)

    # with open(file_path, 'w', encoding='utf-8') as file:
    #     json.dump(index_data, file, ensure_ascii=False, indent=4)
    #     print(f"Data saved to {file_path}")
#----------------------------------------------------------------------
# food_url = f'https://www.10000recipe.com/recipe/list.html'
# webdriver_chrome.get(food_url)
# search_bar = webdriver_chrome.find_element(By.NAME, "q")
food_list =  query
# chat_history = []
# language = input('언어를 선택해 주세요(예: 한국어 혹은 Korean): ')
language = '한국어' #임시(나중에 삭제)
client2 = OpenAI()
num_serving = '1 인분' #임시 (나중에 삭제)
completion = client2.chat.completions.create(
    model = 'gpt-4o-mini',
    messages = [{'role': 'system', 'content': """
    You are a professional chef who knows every ingredient and detailed cooking process for any dish. When given a specific food topic:
    1. Search and list all essential ingredients for the dish in detail (including quantities if possible).
    2. Provide a step-by-step cooking process with precise instructions and tips for achieving the best results.
    3. Use the language of {language} for your answer.
    4. Do NOT use the example below as the answer to the user's question. It is only a reference for the level of detail expected in your response.
    5.When writing the recipe, ensure to mention the number of servings based on the ingredients provided. Use clear formats such as 'serves 2' or 'serves 4'. 
    6. If the user requests a specific number of servings, such as 1 serving, adjust all the ingredients and steps accordingly and the number of serving will be informed by {num_serving}

    **Example (Reference Only):**
    Dish: Pasta (for 4~5 servings)

    **Ingredients:**
    - Pasta (spaghetti or another type) - 400g  
    - Water - 4L  
    - Salt - 2 tablespoons (for boiling water)  
    - Olive oil - 3 tablespoons  
    - Garlic - 4 cloves (minced or thinly sliced)  
    - Onion - 1 medium (diced)  
    - Tomato sauce - 400g (or 4 fresh tomatoes, crushed)  
    - Sugar - 1 teaspoon (to balance acidity)  
    - Parmesan cheese (grated) - 50g  
    - Fresh basil - a few leaves (or 1 teaspoon dried basil)  
    - Black pepper - a pinch (freshly ground)  

    Optional:  
    - Bacon or pancetta - 100g (diced)  
    - Red chili pepper (for spiciness) - 1 piece  

    **Cooking Steps:**
    1. **Boil the Pasta:**  
    - Boil 4L of water in a large pot.  
    - Add 2 tablespoons of salt once the water boils (the water should taste slightly salty).  
    - Cook pasta for 1 minute less than the package instructions (e.g., if recommended time is 10 minutes, cook for 9).  
    - Reserve 1 cup of pasta water, then drain the pasta.  

    2. **Prepare the Sauce:**  
    (A) For Aglio e Olio:  
    - Heat a pan over medium heat and add 3 tablespoons of olive oil.  
    - Sauté garlic slices and diced chili peppers over low heat until fragrant (do not burn).  
    - Add cooked pasta and 2-3 tablespoons of reserved pasta water, tossing until well-coated.  
    - Garnish with fresh basil and grated Parmesan cheese.  

    (B) For Tomato Sauce:  
    - Heat 2 tablespoons of olive oil in a pan over medium heat.  
    - Sauté diced onions until translucent.  
    - Add garlic slices, followed by tomato sauce (or crushed fresh tomatoes).  
    - Season with salt, sugar, and black pepper. Simmer over low heat for 10 minutes.  
    - Add cooked pasta and a small amount of reserved pasta water. Toss until combined.  
    - Garnish with basil and Parmesan cheese before serving.  

    **Serving Tips:**  
    - Plate the pasta and top with extra sauce.  
    - Sprinkle additional Parmesan cheese and garnish with fresh basil leaves.  
    - Serve with freshly ground black pepper and a drizzle of olive oil if desired.  
    
    Now, provide an equally detailed response for the user's specific name ofthe food: {food_list}.
    """},
        {'role' : 'user', 'content' : food_list},
        {'role' : 'user', 'content' : language},
        {'role' : 'user', 'content' : num_serving},
    ]
)
complete_recipe = completion.choices[0].message.content
client3 = OpenAI()
completion = client3.chat.completions.create(
    model = 'gpt-4o-mini',
    messages = [
    {'role': 'system',
    'content': """
    1.1 Identify any additional ingredients, tips, or unique elements that could enhance {complete_recipe}.
    1.2 Add these enhancements to {complete_recipe} as suggestions or optional steps, without altering the original recipe structure.
    1.3 Provide detailed explanations for each suggestion, including:
        - Specific quantities of new ingredients.
        - Clear steps for incorporating them into the recipe.
        - A brief explanation of how each suggestion improves the dish (max of 4 unique enhancements, no duplicates).
    2. **Output Format**: Present the enhanced recipe in the following structure:
        - Original Recipe: {complete_recipe}
        - Enhanced Recipe: List the new steps or ingredients clearly as additions to the original.
        - Explanations: Provide detailed explanations for each enhancement (only unique explanations, no repetition).
    3. **Alternative Ideas**:
        4.1 Below the enhanced recipe, provide a section titled "이건 어때요?" with suggestions for other related recipes or variations based on the topic, incorporating any unique or creative ideas found in {food_details}(which means, you can recommend other food related to the topic).
    4. **총 칼로리**:
        5.1 List the calories for each ingredient in {complete_recipe}, so don't list the ingredient with calories again. and any new ingredients added, directly beside each ingredient (without creating a separate list for calories).
        5.2 Calculate the total calorie count for the final enhanced recipe.
        5.3 Present this information clearly at the end of the enhanced recipe.
    5. **Language: You must use the language of {language} for your answer**.
    6. ***Remove all the duplicated information (all)***.
        
    Full Example:
    Original Recipe: 고구마튀김 (1인분)
    재료:
    고구마 - 1개 (약 150g, 109 칼로리)
    튀김 가루 - 50g (187 칼로리)
    찬물 - 75ml (0 칼로리)
    식물성 기름 (튀김용) - 적당량 (약 250 칼로리)
    소금 - 약간 (0 칼로리)

    조리 과정:
    1. 고구마는 깨끗이 씻어 껍질을 벗긴 후 약 0.5cm 두께로 얇게 슬라이스합니다.
    2. 작은 볼에 튀김 가루를 넣고 찬물을 부어줍니다. 젓가락이나 거품기를 이용해 반죽을 가볍게 섞어줍니다. 반죽에 약간의 덩어리가 있어도 괜찮습니다.
    3. 냄비나 깊은 팬에 기름을 넉넉히 붓고 170-180°C까지 가열합니다. 기름 온도를 확인하려면 반죽을 조금 떨어뜨려보세요. 바로 떠오르면 적당한 온도입니다.
    4. 고구마 슬라이스를 반죽에 담가 고루 묻힌 후, 뜨거운 기름에 하나씩 넣어줍니다. 약 2-3분간, 혹은 고구마가 노릇노릇하고 바삭할 때까지 튀깁니다. 튀긴 고구마는 키친타월에 올려 기름을 제거합니다.\n  5. 튀긴 고구마에 소금을 약간 뿌려 간을 맞춥니다.\n\n  **서빙 팁:** 따뜻할 때 바로 먹는 것이 가장 맛있습니다. 간장이나 칠리 소스를 곁들여 먹으면 더욱 맛있습니다.
    Enhanced Recipe:
    1. 향미 추가: 파슬리가루
    - 추가 재료: 파슬리 가루 1큰술 (3 칼로리)
    - 고구마를 슬라이스하고 반죽을 만들 때 파슬리 가루를 함께 섞어주세요. 시각적 아름다움과 더불어 향긋한 풍미를 더해줍니다.

    2. 조리법 개선: 온도 확인     
    - 반죽을 너무 오래 젓지 않도록 주의하세요. 튀김의 부드러움과 바삭함을 유지하기 위해 살살 저어주는 것이 중요합니다.

    3. 바삭함 유지: 채반 사용
    - 튀긴 고구마를 키친타월 대신 채반에 올려 식히세요. 더 바삭하고 눅눅해지지 않게 유지됩니다.

    4. 색감 강조: 주항빛 고구마 선택
    - 주황빛이 도는 고구마를 사용하면 색감이 더욱 아름답게 나옵니다. 치자물을 들이지 않아도 예쁜 색을 가질 수 있습니다.

    Explanations:
    1. 파슬리가루 추가: 시각적 효과와 향을 더해줍니다. 더 풍부한 맛을 느낄 수 있습니다.
    2. 온도 확인: 반죽을 가볍게 저어 튀김의 바삭함을 극대화합니다.
    3. 바삭함 유지: 튀김이 눅눅해지지 않게 하여 식감 개선
    4. 색감 강조: 요리의 시각적 매력을 높이는 데 기여합니다.

    이건 어때요?
    다양한 고구마 요리를 즐기고 싶다면, 고구마 맛탕이나 고구마전도 시도해보세요. 특별한 날엔 고구마 그라탱도 추천합니다. 새로운 식감과 맛을 경험할 수 있습니다.
    그리고 고구마를 이용한 요리
    **맛탕**
    **고구마 케이크**
    **고구마 튀김**들도 맛있습니다.

    총 칼로리:기존 레시피 총 칼로리는 약 546 칼로리이고, 파슬리가루를 추가하면 총 549 칼로리가 됩니다.
    """},
        {'role' : 'user', 'content' : complete_recipe},
        {'role' : 'user', 'content' : language}
    ]
)