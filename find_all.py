import requests, json
from bs4 import BeautifulSoup
import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
import warnings
warnings.filterwarnings(action = 'ignore')

url = 'https://www.10000recipe.com/recipe/list.html'
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    # 'common_sp_link' 클래스를 가진 요소 찾기
    elements = soup.find_all(class_='common_sp_link')
    if elements:
        print(f"'common_sp_link' 클래스가 {len(elements)}개 발견되었습니다.")
    else:
        print("'common_sp_link' 클래스가 발견되지 않았습니다.")
else:
    print(f"페이지를 불러오는 데 실패했습니다. 상태 코드: {response.status_code}")
    
for i, element in enumerate(elements):
    link = element.get('href', 'No href found')  # href 속성 가져오기
    print(f"{i + 1}: {link}")
    
import requests
from bs4 import BeautifulSoup

# 베이스 URL (페이지 번호를 추가하여 각 페이지로 이동)
base_url = 'https://www.10000recipe.com/recipe/list.html?page='

# 전체 데이터를 저장할 리스트
all_food_data = []

# 1페이지부터 10페이지까지 반복
for page_num in range(1, 11):
    url = f"{base_url}{page_num}"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # 'common_sp_link' 클래스의 요소를 찾아 레시피 링크 추출
        food_list = soup.find_all(attrs={'class': 'common_sp_link'})
        
        # 각 레시피 링크에 대해 데이터를 추출
        for food in food_list:
            food_id = food['href'].split('/')[-1]
            new_url = f'https://www.10000recipe.com/recipe/{food_id}'
            
            # 개별 레시피 페이지 요청
            new_response = requests.get(new_url)
            if new_response.status_code == 200:
                new_soup = BeautifulSoup(new_response.text, 'html.parser')
                food_info = new_soup.find(attrs={'type': 'application/ld+json'})
                
                if food_info:
                    result = json.loads(food_info.text)
                    ingredient = ', '.join(result['recipeIngredient'])
                    recipe = [f"{i + 1}. {result['recipeInstructions'][i]['text']}" for i in range(len(result['recipeInstructions']))]
                    
                    # 레시피 정보 저장
                    food_data = {
                        'name': result.get('name', 'Unknown'),
                        'ingredients': ingredient,
                        'recipe': recipe
                    }
                    all_food_data.append(food_data)
    else:
        print(f"페이지 {page_num}를 불러오는 데 실패했습니다.")

# 모든 페이지의 레시피 데이터 출력
for food in all_food_data:
    print(f"레시피 이름: {food['name']}")
    print(f"재료: {food['ingredients']}")
    print("조리법:")
    for step in food['recipe']:
        print(step)
    print("-" * 50)