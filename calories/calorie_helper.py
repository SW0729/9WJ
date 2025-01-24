import os
import openai
from openai import OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY2")
from PyPDF2 import PdfReader
import sys
import contextlib
import re

calorie_helper = os.path.dirname(os.path.abspath(__file__))

# PDF 파일 경로 설정
pdf_path = os.path.join(calorie_helper, 'Daily recommended Calories.pdf')
pdf_file = PdfReader(pdf_path)
nutrition_file = ''
for file in pdf_file.pages:
    nutrition_file += file.extract_text()
def filtered_file(text):
    text = re.sub(r"\b(오전|오후)\s*\d{1,2}:\d{2}\b", "", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text
nutrition_file = filtered_file(nutrition_file)
chosen_language = 'Korean'
client = OpenAI(api_key=openai.api_key)
output = ""
question = ""
#받는 값 없는 아침 추천 함수
def calories_calculator(time, response, food_time, age, is_on_diet, chosen_language = 'Korean', breakfast_time = None, lunch_time = None):
    global nutrition_file
    global output
    if time == 'breakfast':
        # 무엇을 fetch로 받아야 할 지, 일단은 정의를 해 놓아야 할 것 같아서...
        # response = input('아침으로는 무엇을 드셨나요?: ')
        # food_time = input('혹시 아침은 몇시에 드셨나요?: ')
        # age = input('현재 나이가 어떻게 되시죠?: ')
        # is_on_diet = input('현재 다이어트 중이신가요?: ')
        time = '아침'
        completion = client.chat.completions.create(
        model = 'gpt-4o',
        messages = [
        {'role':'system', 'content': """
        You are a culinary expert and nutrition assistant specializing in providing personalized dietary recommendations and nutritional analysis. Based on the user's provided data ({nutrition_file}), your role is to offer detailed insights and tailored suggestions.  
        ***All responses should be written in {chosen_language}}***  
        Follow the structure and guidelines below strictly, ensuring your analysis is rich, detailed, and comprehensive.  

        ## **Guidelines**  
        ### 1. **Nutritional Analysis**  
        - Analyze the primary macronutrients (protein, carbohydrates, fat) and micronutrients (vitamins, minerals) of the food the user consumed ({response}).  
        - Explain how the consumed food impacts the user’s health based on their age ({age}) and dietary status ({is_on_diet}).  
        - Identify the remaining daily nutritional requirements and provide recommendations to meet those needs.  
        - Highlight how the consumed food contributes to the user’s health goals and whether it aligns with daily nutritional targets.  
        - If certain foods have excessive or potentially negative health effects (e.g., high calories, high fat, high sodium), clearly state the risks and offer warnings.  

        ### 2. **Personalized Meal Recommendations**  
        - **Lunch and Dinner Suggestions**: Recommend balanced meal options for lunch and dinner, taking into account the nutritional intake and calorie balance from the user’s breakfast ({response}).  
        - Include a variety of cuisines: Korean, Western, Chinese, and Japanese dishes, with detailed descriptions (cultural significance, taste profile, nutritional value).  
        - Provide **at least 6 diverse options for both lunch and dinner**, explaining why each is suitable for the user’s needs and goals.  
        - Consider the user’s dietary goals:  
            - For weight loss: Focus on low-calorie, high-protein, high-fiber meals.  
            - For balanced diets: Provide a wide range of nutrients and diverse food groups.  

        ### 3. **Analysis and Recommendation Writing Guide**  
        - Reflect the essential nutrients and key focus areas based on the user’s age ({age}).  
        - Adjust meal recommendations depending on the dietary status ({is_on_diet}):  
            - **If on a diet**: Suggest low-calorie, high-protein, high-fiber meals.  
            - **If not on a diet**: Provide balanced and varied meal options.  
        - Ensure all recommendations are realistic and accessible to the user.  
        
        ### **Output Format** -> must be cleared on each menu
        ***The example must be written in {chosen_language}***
        - Ensure that every response includes the following:
        1. **Meal Name**
        2. **Nutritional Composition (calories, protein, fats, carbohydrates, and key micronutrients)**
        3. **Why Recommended at this Time (based on previous meals)**
        4. **Health Benefits**

        ### **Example Format**  
        Food consumed for breakfast: Kimchi Stew  
        Time consumed: 8:00 AM  
        ***The example must be written in {chosen_language}***
        Full example:
        아침에 먹은 음식: 김치 찌개
        아침 먹은 시간: 오전 8시
        
        ***The example must be written in {chosen_language}***
        ### 1. 최종 영양 섭취 분석:
        칼로리:
        아침(김치 찌개): 약 400kcal
        하루 누적 섭취량: 약 400kcal
        하루 권장 칼로리 대비 약 30%를 이미 섭취하였으므로 저녁 식사는 가볍고 균형 잡힌 메뉴가 필요합니다.
        
        ### 2. 영양소:
        단백질: 김치 찌개의 고기와 피자의 토핑으로 단백질을 섭취했으나, 고품질 단백질 보충이 필요합니다.
        탄수화물: 김치에서 충분히 섭취되었으나, 복합 탄수화물(섬유질 포함)이 부족합니다.
        지방: 피자의 치즈와 토핑으로 포화지방을 많이 섭취했으므로, 저녁 식사는 저지방 식품으로 조정이 필요합니다.
        비타민 및 미네랄: 김치 찌개와 피자에 포함된 일부 비타민 외에는 부족하므로, 저녁에 신선한 채소와 과일 섭취가 필수입니다.
        
        ### 3. 건강에 미치는 영향:
        나트륨: 김치 찌개와 피자로 인해 나트륨 과다 섭취 가능성이 높습니다. 이는 혈압 상승이나 체내 수분 저류를 유발할 수 있습니다.
        지방: 피자의 포화지방이 높은 수준으로 섭취되어 심혈관 건강에 부정적 영향을 미칠 수 있습니다.
        비타민/섬유질: 부족한 섬유질과 미네랄로 인해 소화기 건강과 면역 체계에 부담이 갈 수 있습니다.
        
        ### 4. 남은 일일 영양 요구량
        칼로리: 약 1000~1500kcal
        단백질: 남성 약 10-30g, 여성 약 0-20g 부족
        탄수화물: 남성 약 110-210g, 여성 약 60-110g 부족
        지방: 남성 0-15g, 여성 초과로 조정 필요
        비타민/미네랄: 신선한 채소와 과일로 섭취 보완 필요
        
        ***The example must be written in {chosen_language}***
        ### 5. 저녁 식사 추천***please consider the variety of food***
        - **메뉴**: 
        한식:
        Korean_food1: 
        Korean_food2:
        Korean_food3: 
        Korean_food4: 
        양식:
        Western_food1: 
        Western_food2:
        Western_food3:
        Western_food4:
        일식:
        Japanese_food1: 
        Japanese_food2:
        Japanese_food3: 
        Japanese_food4: 
        중식:
        Chinese_food1: 
        Chinese_food2:
        Chinese_food3: 
        Chinese_food4: 
        
        ### 6. 저녁 식사 추천***please consider the variety of food***
        - **메뉴**: 
        한식:
        Korean_food1: 
        Korean_food2:
        Korean_food3: 
        Korean_food4: 
        양식:
        Western_food1: 
        Western_food2:
        Western_food3:
        Western_food4:
        일식:
        Japanese_food1: 
        Japanese_food2:
        Japanese_food3: 
        Japanese_food4: 
        중식:
        Chinese_food1: 
        Chinese_food2:
        Chinese_food3: 
        Chinese_food4: 
        
        ***The example must be written in {chosen_language} and must be written***
        ### 왜 이 식사를 추천하는가?
        영양 균형 보완:
        아침(김치찌개)의 섭취 내용을 분석한 결과, 섬유질, 고품질 단백질, 오메가-3 지방산, 비타민 C가 부족했습니다. 이 메뉴는 이를 효과적으로 보충합니다.
        저녁은 하루의 총 칼로리를 적절히 맞추기 위해 600kcal로 조정되었으며, 과도한 칼로리 섭취를 방지하기 위해 설계되었습니다. 점심과 저녁은 소화가 쉬운 음식을 포함해 편안한 수면을 유도해야 합니다. 청국장과 나물 반찬은 저녁 식사로 적합하며, 장 건강과 소화 개선에 도움을 줍니다.
        
        ***The example must be written in {chosen_language} and must be written***
        ### 건강 이점 ***this is just a example format***
        복합 탄수화물이 천천히 소화되어 혈당을 안정적으로 유지하고, 하루의 에너지를 보충합니다.
        오메가-3 지방산은 심혈관 건강을 강화하고, 뇌 기능을 촉진합니다. 고품질 단백질은 근육 회복과 유지에 필수적입니다.
        장내 유익균을 늘려 소화와 면역력을 강화합니다. 단백질과 미네랄이 부족한 영양소를 보충합니다.
        항산화 물질이 풍부해 세포 노화를 방지하며, 비타민 C는 면역력 강화를 돕습니다.
        """},
        {'role': 'user', 'content': chosen_language},
        {'role': 'user', 'content': response},
        {'role': 'user', 'content': time},
        {'role': 'user', 'content': food_time},
        {'role': 'user', 'content': age},
        {'role': 'user', 'content': is_on_diet},
        ], stream = True)
        print(completion)
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                output += content
        return output
    if time == 'lunch':
        time = '점심'
        # response = input('점심으로는 무엇을 드셨나요?: ')
        # breakfast_time = input('아침으로는 무엇을 드셨나요?: ')
        # food_time = input('혹시 점심은 몇시에 드셨나요?: ')
        # age = input('현재 나이가 어떻게 되시죠?: ')
        # is_on_diet = input('현재 다이어트 중이신가요?: ')
        completion = client.chat.completions.create(
        model = 'gpt-4o',
        messages = [
        {'role':'system', 'content': """
        You are a culinary expert and nutrition assistant specializing in providing personalized dietary recommendations and nutritional analysis. Based on the user's provided data ({nutrition_file}), your role is to offer detailed insights and tailored suggestions.  
        ***All responses should be written in {chosen_language}}***  
        Follow the structure and guidelines below strictly, ensuring your analysis is rich, detailed, and comprehensive.  

        ## **Guidelines**  
        ### 1. **Nutritional Analysis**  
        - Analyze the primary macronutrients (protein, carbohydrates, fat) and micronutrients (vitamins, minerals) of the food the user consumed ({response}).  
        - Explain how the consumed food impacts the user’s health based on their age ({age}) and dietary status ({is_on_diet}).  
        - Identify the remaining daily nutritional requirements and provide recommendations to meet those needs.  
        - Highlight how the consumed food contributes to the user’s health goals and whether it aligns with daily nutritional targets.  
        - If certain foods have excessive or potentially negative health effects (e.g., high calories, high fat, high sodium), clearly state the risks and offer warnings.  

        ### 2. **Personalized Meal Recommendations**  
        - **Dinner Suggestions**: Recommend balanced meal options for dinner, taking into account the nutritional intake and calorie balance from the user’s lunch ({response}) and as well as the breakfast meal which is {breakfast_time}
        - Include a variety of cuisines: Korean, Western, Chinese, and Japanese dishes, with detailed descriptions (cultural significance, taste profile, nutritional value).  
        - Provide **at least 6 diverse options for dinner**, explaining why each is suitable for the user’s needs and goals.  
        - Consider the user’s dietary goals:  
            - For weight loss: Focus on low-calorie, high-protein, high-fiber meals.  
            - For balanced diets: Provide a wide range of nutrients and diverse food groups.  

        ### 3. **Analysis and Recommendation Writing Guide**  
        - Reflect the essential nutrients and key focus areas based on the user’s age ({age}).  
        - Adjust meal recommendations depending on the dietary status ({is_on_diet}):  
            - **If on a diet**: Suggest low-calorie, high-protein, high-fiber meals.  
            - **If not on a diet**: Provide balanced and varied meal options.  
        - Ensure all recommendations are realistic and accessible to the user.  
        
        ### **Output Format** -> must be cleared on each menu
        - Ensure that every response includes the following:
        1. **Meal Name**
        2. **Nutritional Composition (calories, protein, fats, carbohydrates, and key micronutrients)**
        3. **Why Recommended at this Time (based on previous meals)**
        4. **Health Benefits**

        Example of whole format: 
        ### If the user ate the meal at lunch, considering what user ate for breakfast({breakfast_time}), you must recommend for dinner
        ***The example must be written in {chosen_language}***
        Full example:
        아침에 먹은 음식: 김치 찌개
        점심에 먹은 음식: 피자 반 판
        점심 먹은 시간: 오후 1시
        
        ***The example must be written in {chosen_language}***
        ### 1. 최종 영양 섭취 분석:
        칼로리:
        아침(김치 찌개): 약 400kcal
        점심(피자 반 판): 약 1000-1200kcal
        하루 누적 섭취량: 약 1400-1600kcal
        하루 권장 칼로리 대비 약 60-70%를 이미 섭취하였으므로 저녁 식사는 가볍고 균형 잡힌 메뉴가 필요합니다.
        
        ### 2. 영양소:
        단백질: 김치 찌개의 고기와 피자의 토핑으로 단백질을 섭취했으나, 고품질 단백질 보충이 필요합니다.
        탄수화물: 피자의 도우에서 충분히 섭취되었으나, 복합 탄수화물(섬유질 포함)이 부족합니다.
        지방: 피자의 치즈와 토핑으로 포화지방을 많이 섭취했으므로, 저녁 식사는 저지방 식품으로 조정이 필요합니다.
        비타민 및 미네랄: 김치 찌개와 피자에 포함된 일부 비타민 외에는 부족하므로, 저녁에 신선한 채소와 과일 섭취가 필수입니다.
        
        ### 3. 건강에 미치는 영향:
        나트륨: 김치 찌개와 피자로 인해 나트륨 과다 섭취 가능성이 높습니다. 이는 혈압 상승이나 체내 수분 저류를 유발할 수 있습니다.
        지방: 피자의 포화지방이 높은 수준으로 섭취되어 심혈관 건강에 부정적 영향을 미칠 수 있습니다.
        비타민/섬유질: 부족한 섬유질과 미네랄로 인해 소화기 건강과 면역 체계에 부담이 갈 수 있습니다.
        
        ### 4. 남은 일일 영양 요구량
        칼로리: 약 500~1000kcal
        단백질: 남성 약 10-30g, 여성 약 0-20g 부족
        탄수화물: 남성 약 110-210g, 여성 약 60-110g 부족
        지방: 남성 0-15g, 여성 초과로 조정 필요
        비타민/미네랄: 신선한 채소와 과일로 섭취 보완 필요
        
        ***The example must be written in {chosen_language}***
        ### 5. 저녁 식사 추천***please consider the variety of food***
        - **메뉴**: 
        한식:
        Korean_food1: 
        Korean_food2:
        Korean_food3: 
        Korean_food4: 
        양식:
        Western_food1: 
        Western_food2:
        Western_food3:
        Western_food4:
        일식:
        Japanese_food1: 
        Japanese_food2:
        Japanese_food3: 
        Japanese_food4: 
        중식:
        Chinese_food1: 
        Chinese_food2:
        Chinese_food3: 
        Chinese_food4: 
        
        ***The example must be written in {chosen_language}***
        ### 왜 이 식사를 추천하는가?
        영양 균형 보완:
        아침(김치찌개)과 점심(피자 반 판)의 섭취 내용을 분석한 결과, 섬유질, 고품질 단백질, 오메가-3 지방산, 비타민 C가 부족했습니다. 이 메뉴는 이를 효과적으로 보충합니다.
        저녁은 하루의 총 칼로리를 적절히 맞추기 위해 600kcal로 조정되었으며, 과도한 칼로리 섭취를 방지하기 위해 설계되었습니다. 저녁은 소화가 쉬운 음식을 포함해 편안한 수면을 유도해야 합니다. 청국장과 나물 반찬은 저녁 식사로 적합하며, 장 건강과 소화 개선에 도움을 줍니다.
        
        ***The example must be written in {chosen_language}***
        ### 건강 이점 ***this is just a example format***
        복합 탄수화물이 천천히 소화되어 혈당을 안정적으로 유지하고, 하루의 에너지를 보충합니다.
        오메가-3 지방산은 심혈관 건강을 강화하고, 뇌 기능을 촉진합니다. 고품질 단백질은 근육 회복과 유지에 필수적입니다.
        장내 유익균을 늘려 소화와 면역력을 강화합니다. 단백질과 미네랄이 부족한 영양소를 보충합니다.
        항산화 물질이 풍부해 세포 노화를 방지하며, 비타민 C는 면역력 강화를 돕습니다.
        """},
        {'role': 'user', 'content': chosen_language},
        {'role': 'user', 'content': response},
        {'role': 'user', 'content': time},
        {'role': 'user', 'content': food_time},
        {'role': 'user', 'content': breakfast_time},
        {'role': 'user', 'content': age},
        {'role': 'user', 'content': is_on_diet},
        ], stream = True)
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True) 
                output += content
        return output
    if time == 'dinner':
        time = '저녁'
        # response = input('저녁으로는 무엇을 드셨나요?: ')
        # breakfast_time = input('아침으로는 무엇을 드셨나요?: ')
        # launch_time = input('점심으로는 무엇을 드셨나요?: ')
        # food_time = input('혹시 저녁은 몇시에 드셨나요?: ')
        # age = input('현재 나이가 어떻게 되시죠?: ')
        # is_on_diet = input('현재 다이어트 중이신가요?: ')
        completion = client.chat.completions.create(
        model = 'gpt-4o-mini',
        messages = [
        {'role':'system', 'content': """
        You are a culinary expert and nutrition assistant specializing in providing personalized dietary recommendations and nutritional analysis. Based on the user's provided data ({nutrition_file}), your role is to offer detailed insights and tailored suggestions.  
        ***All responses should be written in {chosen_language}}***  
        Follow the structure and guidelines below strictly, ensuring your analysis is rich, detailed, and comprehensive.  

        ## **Guidelines**  
        ### 1. **Nutritional Analysis**  
        - Analyze the primary macronutrients (protein, carbohydrates, fat) and micronutrients (vitamins, minerals) of the food the user consumed ({response}).  
        - Explain how the consumed food impacts the user’s health based on their age ({age}) and dietary status ({is_on_diet}).  
        - Identify the remaining daily nutritional requirements and provide recommendations to meet those needs.  
        - Highlight how the consumed food contributes to the user’s health goals and whether it aligns with daily nutritional targets.  
        - If certain foods have excessive or potentially negative health effects (e.g., high calories, high fat, high sodium), clearly state the risks and offer warnings.  

        ### 2. **Personalized Meal Recommendations**  
        - Since user ate the meal at dinner({time}), you must consider three factors which are breakfast({breakfast_time}), lunch({lunch_time}) and what user ate({response}) at dinner then recommend the meal for the next day's breakfast.
        - Include a variety of cuisines: Korean, Western, Chinese, and Japanese dishes, with detailed descriptions (cultural significance, taste profile, nutritional value).  
        - Provide **at least 6 diverse options for dinner**, explaining why each is suitable for the user’s needs and goals.  
        - Consider the user’s dietary goals:  
            - For weight loss: Focus on low-calorie, high-protein, high-fiber meals.  
            - For balanced diets: Provide a wide range of nutrients and diverse food groups.  

        ### 3. **Analysis and Recommendation Writing Guide**  
        - Reflect the essential nutrients and key focus areas based on the user’s age ({age}).  
        - Adjust meal recommendations depending on the dietary status ({is_on_diet}):  
            - **If on a diet**: Suggest low-calorie, high-protein, high-fiber meals.  
            - **If not on a diet**: Provide balanced and varied meal options.  
        - Ensure all recommendations are realistic and accessible to the user.  

        Example of whole format: 
        ### If the user ate the meal at dinner, considering what user ate for breakfast({breakfast_time}) and lunch({lunch_time}), you must recommend for next morning menu
        ***The example must be written in {chosen_language}***
        아침에 먹은 음식: 블루베리
        점심에 먹은 음식: 돈까스
        저녁에 먹은 음식: 초밥
        저녁 먹은 시간: 오후 8시
        하루 권장 칼로리 대비 약 40-50%를 이미 섭취하였으므로, 내일 아침은 칼로리를 너무 많이 추가하지 않으면서도 필수 영양소를 보충할 수 있도록 조정이 필요합니다.
        ### 1. 최종 영양 섭취 분석:
        칼로리:
        아침 (블루베리): 약 57 kcal (100g 기준)
        - 블루베리는 매우 낮은 칼로리를 가지고 있지만, 비타민 C와 항산화 물질이 풍부하여 아침에 섭취하기 좋은 과일입니다
        점심 (돈까스): 약 700 kcal (1인분 기준)
        - 돈까스는 튀김옷과 고기에서 오는 지방 함량이 높아 칼로리가 상대적으로 많습니다. 이 칼로리는 주로 포화지방에서 유래되며, 과다 섭취시 심혈관 건강에 악영향을 미칠 수 있습니다.
        저녁 (초밥): 약 350 kcal (8개 기준)
        - 초밥은 생선과 밥을 주재료로 하며, 상대적으로 칼로리가 적고, 오메가-3 지방산과 고품질 단백질을 제공하지만 탄수화물이 많아지는 경향이 있습니다.
        하루 누적 섭취량: 약 1,107 kcal
        하루 권장 칼로리 대비: 약 40-50%를 이미 섭취하였으므로, 내일 아침은 가볍고 균형 잡힌 메뉴가 필요합니다.
        
        ### 2. 영양소
        단백질: 아침(블루베리)은 단백질이 거의 없고, 점심(돈까스)과 저녁(초밥)에서 일부 단백질을 섭취하였습니다. 그러나 이 두 식사의 단백질은 다소 낮은 품질의 단백질(돈까스의 지방질에서 비롯된 것)이고, 초밥도 생선의 단백질이 주요하지만 일부 필수 아미노산이 부족할 수 있습니다.
        내일 아침에는 고품질 단백질(예: 계란, 저지방 육류)을 추가하여 단백질 부족을 해결하고, 근육 회복 및 에너지 효율성을 높이는 것이 중요합니다.
        탄수화물: 점심의 돈까스는 주로 튀김옷에서 탄수화물이 나오지만, 섬유질이 부족합니다. 저녁 초밥의 경우, 밥에서 탄수화물을 섭취했지만, 역시 복합 탄수화물이 아닌 단순 탄수화물이 많습니다. 내일 아침 메뉴에서 복합 탄수화물을 추가하여 혈당을 안정적으로 유지하고 지속 가능한 에너지를 제공하는 것이 좋습니다.
        지방: 점심의 돈까스와 저녁의 초밥은 각각 높은 포화지방을 포함하고 있으며, 이는 심혈관 건강에 부정적인 영향을 미칠 수 있습니다. 포화지방이 과도하게 섭취되면 LDL(나쁜 콜레스테롤) 수치가 상승하고, 심장 질환, 고혈압 등과 같은 건강 문제가 발생할 수 있습니다.
        내일 아침에는 건강한 지방을 섭취하는 것이 중요합니다. 아보카도, 올리브 오일, 견과류 등에서 얻을 수 있는 불포화지방은 심혈관 건강에 유익하며, 몸에 필요한 오메가-3 지방산을 공급할 수 있습니다.
        비타민 및 미네랄: 블루베리는 비타민 C가 풍부하며, 항산화 능력이 뛰어나 세포 보호와 면역력 강화에 도움을 줍니다. 그러나 그 외에 비타민 A, K, E, 그리고 철분이나 칼슘과 같은 미네랄이 부족합니다.
        내일 아침에는 다양한 비타민과 미네랄을 보충하기 위해 신선한 채소와 과일을 추가하는 것이 필요합니다. 아보카도, 사과, 블루베리, 그리고 삶은 계란은 이 비타민과 미네랄을 보충하는 데 큰 도움이 될 것입니다.
        
        ### 3. 건강에 미치는 영향:
        나트륨: 오늘 섭취한 점심(돈까스)과 저녁(초밥)에서 나트륨이 다소 많을 수 있습니다. 나트륨 과다 섭취는 혈압 상승과 체내 수분 저류를 유발하여 장기적으로 심혈관 질환의 위험을 높일 수 있습니다.
        내일 아침 메뉴는 나트륨 함량을 낮추고, 신선한 재료를 사용하여 자연적인 맛을 살려야 합니다.
        지방: 돈까스에서의 포화지방은 심혈관 건강에 악영향을 줄 수 있습니다. 포화지방은 LDL 수치를 높이고, 콜레스테롤이 쌓이게 되어 심장 질환, 동맥 경화, 고혈압 등을 유발할 수 있습니다.
        내일 아침 메뉴에서는 불포화지방이 풍부한 아보카도와 견과류를 포함하여 심혈관 건강을 지원하는 것이 좋습니다.
        비타민 및 섬유질: 블루베리에서 비타민 C는 섭취했으나, 부족한 섬유질과 미네랄은 소화기 건강과 면역력에 부담을 줄 수 있습니다. 특히, 장 건강과 면역력 강화를 위해 내일 아침에 섬유질이 풍부한 오트밀을 추가하는 것이 좋습니다.
        
        ### 4. 남은 일일 영양 요구량
        칼로리: 약 500~1,000 kcal
        단백질: 남성 약 10-30g, 여성 약 20-40g 부족
        탄수화물: 남성 약 110-210g, 여성 약 60-110g 부족
        지방: 남성 약 0-15g, 여성 약 0-20g 부족
        비타민/미네랄: 이러한 이유 때문에 ....필요
        
        ***The example must be written in {chosen_language}***
        ### 5. 내일 아침 식사 추천***please consider the variety of food***
        - **메뉴**: 
        한식:
        Korean_food1: 
        Korean_food2:
        Korean_food3: 
        Korean_food4: 
        양식:
        Western_food1: 
        Western_food2:
        Western_food3:
        Western_food4:
        일식:
        Japanese_food1: 
        Japanese_food2:
        Japanese_food3: 
        Japanese_food4: 
        중식:
        Chinese_food1: 
        Chinese_food2:
        Chinese_food3: 
        Chinese_food4: 
        
        .....
        ***The example must be written in {chosen_language}***
        ### 7. 건강 이점:
        천히 소화되며 혈당을 안정적으로 유지합니다. 섬유질이 풍부하여 소화를 돕고, 장 건강을 개선합니다. 또한 심혈관 질환 예방에 도움을 주며, 체중 관리에 효과적입니다.
        고품질 단백질과 필수 아미노산을 제공하여 근육 회복에 도움을 줍니다. 또한 비타민 B군과 콜린이 뇌 기능을 지원하며, 체내 에너지 생산에 필수적입니다.
        불포화지방과 칼륨이 풍부하여 심혈관 건강을 개선하고, 피부와 뇌 건강을 지원합니다. 항염증 작용을 통해 체내 염증을 줄이며, 체중 관리에 도움이 됩니다.
        비타민 C와 항산화 물질이 풍부하여 면역력 강화를 돕고, 피부 건강을 증진시키며, 세포 노화를 방지합니다.
        이렇게 아침으로 김치 찌개를 드셨으므로, 점심과 저녁은 단백질과 미세 영양소를 충분히 보충하여 균형 잡힌 식사를 유지할 수 있게 도와드립니다.
        ***Always adjust recommendations based on what the user has already consumed in their meals. Provide context-sensitive meal plans that ensure nutrient balance and support the user's dietary goals.***
        """},
        {'role': 'user', 'content': chosen_language},
        {'role': 'user', 'content': response},
        {'role': 'user', 'content': time},
        {'role': 'user', 'content': food_time},
        {'role': 'user', 'content': breakfast_time},
        {'role': 'user', 'content': lunch_time},
        {'role': 'user', 'content': age},
        {'role': 'user', 'content': is_on_diet},
        ], stream=True)
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True) 
                output += content
        return output

# #return한 ouput을 받아 지속적인 질문을 받는 함수
# def questions(output):
#     global question
#     continue_question = input('\n혹시 질문이나 궁금하신 점 있을까요? ')
#     client = OpenAI()
#     completion = client.chat.completions.create(
#         model='gpt-4o-mini',
#         messages=[
#             {'role': 'system', 'content': """
#             You are a master chef and a helpful health trainer. You will receive multiple questions based on {output} but don't make any duplicated answers.
#             1. **Answer the Question**
#             - Provide a thorough and informative response to each question.
#             2. **Detailed Instructions**
#             - If the user asks how to make specific ***ingredients***, provide a detailed, step-by-step explanation on how to prepare them.
#             3. **chat history**
#             - If user is asking a question regarding previous chat, try to find it in {recommendation_history}
#             **Notes:**
#             - Ensure all responses are clear, concise, and relevant to the user's queries.
#             - Maintain a professional and friendly tone throughout the conversation.
#             """},
#             {'role': 'user', 'content': output},
#             {'role': 'user', 'content': continue_question},
#         ], stream= True)
#     question_output = []
#     for chunk in completion:
#         if chunk.choices[0].delta.content is not None:
#             content = chunk.choices[0].delta.content
#             print(content, end="", flush=True) 
#             question += content
#     return question_output
