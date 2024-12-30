import requests, json
from bs4 import BeautifulSoup

def food_info():
    url = f'https://www.10000recipe.com/recipe/list.html'
    response = requests.get(url)
    food_data = []
    if response.status_code == 200:
        try:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
        except Exception as e:
            print("잘못된 요청입니다. 에러:", {e} )
            return
    
