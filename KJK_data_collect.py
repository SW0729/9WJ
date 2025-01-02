from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
#----------------------------------------------------------------------
import requests, json
from bs4 import BeautifulSoup
import os
import openai
from openai import OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY2")
import warnings
warnings.filterwarnings(action = 'ignore')
#----------------------------------------------------------------------

webdriver_options = Options()
webdriver_options.add_argument("--headless")  
driver_service = Service(ChromeDriverManager().install()) 

webdriver_chrome = webdriver.Chrome(service=driver_service, options=webdriver_options)

food_url = f'https://www.10000recipe.com/recipe/list.html'
webdriver_chrome.get(food_url)
search_bar = webdriver_chrome.find_element(By.NAME, "q")

chat_history = []
language = input('언어를 선택해 주세요(예: 한국어 혹은 Korean): ')
while True:
    food_name = input('찾으시는 레시피가 있으실까요: ')
    if food_name.lower() == 'exit':
        break
    print(f'{food_name}에 대한 검색 결과에요!')
    if food_name or another_food_name:
        client = OpenAI()
        completion = client.chat.completions.create(
            model = 'gpt-4o',
            messages = [
                {'role' : 'system', 'content' : """You are an AI with extensive knowledge of all types of food. 
                Your task is to provide a comprehensive list of all subcategories or variations of a given food name(maximum of 7). 
                Focus on listing the most popular and widely recognized subcategories first. 
                Keep the categories at a general or mid-level of detail (e.g., 'cream pasta' 'spaghetti').
                If no subcategories or variations exist, simply return the food name itself. 
                If the input is not a food name or is unrelated to food, respond with 'please type a proper name of food.'
                You must use the language of {language}.
                For last, ***you should not say anything else except your comments***"""},
                {'role' : 'user', 'content' : food_name},
                {'role' : 'assistant', 'content' : """
                example:
                food name : pasta
                answer : 
                1. Cream Pasta
                2. Spaghetti
                3. Tomato Pasta
                4. Lasagna
                5. Pesto Pasta
                """}
            ])
        filtered_name = completion.choices[0].message.content
        print(filtered_name)
        if filtered_name == 'please type a proper name of food.':
            print('음식 이름을 제대로 기입해주세요!')
            continue
        if food_name == filtered_name:
            food_name = filtered_name
        else:
            print("주어진 번호나(예: 1, 2, 3...), 정확한 카테고리의 이름을 선택해 주세요!")
            selected_input = input("선택: ").strip()
            options = [line.split('. ', 1)[-1].strip() for line in filtered_name.split('\n') if '.' in line]
            if selected_input.isdigit():
                tags_num = int(selected_input) - 1
                if 0 <= tags_num < len(options):
                    food_name = options[tags_num]
                    print(food_name)
                else:
                    print("정확한 번호를 선택해 주세요!")
                    continue
            elif selected_input in options:
                food_name = selected_input
                print(food_name)
            else:
                print("정확한 이름을 선택해 주세요!")
                continue
        search_bar.send_keys(food_name)
        search_bar.submit()
        webdriver_chrome.implicitly_wait(300)
        results = webdriver_chrome.find_elements(By.CSS_SELECTOR, "a")
        food_link = results[0].get_attribute("href") if results else None
        print(food_link)
        food_data = []
        food_count = 0
        webdriver_chrome.quit()
        response = requests.get(food_link)
        if response.status_code == 200:
            try:
                food_link_text = response.text
                soup = BeautifulSoup(food_link_text, 'html.parser')
            except Exception as e:
                print("잘못된 요청입니다. 에러:", {e} )
        food_info = soup.find_all(attrs= {'class' : 'common_sp_link'})
        for food in food_info:
            food_id = food['href'].split('/')[-1]
            food_recipe = f'https://www.10000recipe.com/recipe/{food_id}'
            food_recipe_response = requests.get(food_recipe)
            if food_recipe_response.status_code == 200:
                try:
                    food_recipe_soup = BeautifulSoup(food_recipe_response.text, 'html.parser')
                    food_recipe_information = food_recipe_soup.find(attrs = {'type' : 'application/ld+json'})
                except Exception as e:
                    print(f'조회에 실패했습니다, 이유: {e}')
                if food_recipe_information:
                    try:
                        food_details = json.loads(food_recipe_information.text)
                        title = food_details.get('name','이름 없음')
                        ingredients = food_details.get("recipeIngredient", [])
                        instructions = [
                            step.get("text", "단계 없음") for step in food_details.get("recipeInstructions", [])
                        ]
                        food_count += 1
                        food_data.append({
                            "제목": title,
                            "재료": ingredients,
                            "설명": instructions
                        })
                    except Exception as e:
                            print(f'가져오는데 실패했습니다. 이유: {e}')
                    if food_count == 15:
                        # client1 = OpenAI()
                        # completion = client1.chat.completions.create(
                        #     model = 'gpt-4o',
                        #     messages = [
                        #         {'role' : 'system', 'content' : """You will receive multiple titles. Your task is to analyze these titles and create a single, 
                        #         unified title that captures the core meaning and essence of all the given titles.
                        #         Example 1:
                        #         Titles no.1 : 대박 맛집 김치찌개, 아주 맛있는 김치찌개 끓이기, 돼지고기 김치찌개 달인이 되는 황금레시피, 돼지고기 김치찌개 맛내는 비법
                        #         ***Answer = 김치찌게 <- because they all focused on this topic***
                        #         ***language example
                        #         if answer = 김치찌게, language = English then final answer = KimChi soup
                                
                        #         Example 2:
                        #         Titles no.2 : 맛있는 돼지고기 김치찌개, 아주 맛있는 돼지고기 김치찌개 끓이기, 돼지고기 김치찌개 달인이 되는 황금레시피, 돼지고기 김치찌개 맛내는 비법
                        #         ***Answer = 돼지고기 김치찌게 <- because they all focused on this topic***
                        #         ***language example
                        #         if answer = 돼지고기 김치찌게, language = English then final answer = Pork KimChi soup
                                
                        #         Example 3:
                        #         Titles no.3 : 짜파게티 맛있게 끓이는법, 중국집st' 레시피, 짜파게티 요리 / 짜파게티 맛있게 끓이는 법, 짜파게티 52만배 맛있게 먹는 방법, 간단하게 매콤한 짜파게티
                        #         ***Answer = 짜파게티 <- because they all focused on this topic***
                        #         answer = 짜파게티, language = English, final answer = Chapagetti
                        #         ***You must use the language of {language} for the answer***"""},
                        #         {'role' : 'user', 'content' : title},
                        #         {'role' : 'assistant', 'content': """
                        #         """}
                        #     ]
                        # )
                        title_answer = completion.choices[0].message.content
                        client2 = OpenAI()
                        completion = client2.chat.completions.create(
                            model = 'gpt-4o',
                            messages = [{'role': 'system', 'content': """
                            You are a professional chef who knows every ingredient and detailed cooking process for any dish. When given a specific food topic:
                            1. Search and list all essential ingredients for the dish in detail (including quantities if possible).
                            2. Provide a step-by-step cooking process with precise instructions and tips for achieving the best results.
                            3. Use the language of {language} for your answer.
                            4. Do NOT use the example below as the answer to the user's question. It is only a reference for the level of detail expected in your response.

                            **Example (Reference Only):**
                            Dish: Pasta (for 4 servings)

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
                            
                            Now, provide an equally detailed response for the user's specific name ofthe food: {food_name}.
                            """},
                                {'role' : 'user', 'content' : food_name},
                                {'role' : 'user', 'content' : language},
                            ]
                        )
                        complete_recipe = completion.choices[0].message.content
                        client3 = OpenAI()
                        completion = client3.chat.completions.create(
                            model = 'gpt-4o',
                            messages = [
                            {'role': 'system',
                            'content': """
                            You will receive two inputs: {complete_recipe} and {food_details}.
                            1. **Comparison Task**: Start by comparing {complete_recipe} with each recipe in {food_details}. This is only for analysis, to identify differences or enhancements.
                            2. **Enhancement Task**: Use {complete_recipe} as the base recipe (do not replace it), and refer to {food_details} to create an enhanced version of {complete_recipe}(which mean, you must improve {complete_recipe} using {food_details}).
                            2.1 Identify any additional ingredients, tips, or unique elements in {food_details} that could enhance {complete_recipe}.
                            2.2 Add these enhancements to {complete_recipe} as suggestions or optional steps, without altering the original recipe structure.
                            2.3 Provide detailed explanations for each suggestion, including:
                                - Specific quantities of new ingredients.
                                - Clear steps for incorporating them into the recipe.
                                - A brief explanation of how each suggestion improves the dish (max of 4 unique enhancements, no duplicates).
                            3. **Output Format**: Present the enhanced recipe in the following structure:
                                - Original Recipe: {complete_recipe}
                                - Enhanced Recipe: List the new steps or ingredients clearly as additions to the original.
                                - Explanations: Provide detailed explanations for each enhancement (only unique explanations, no repetition).
                            4. **Alternative Ideas**:
                                4.1 Below the enhanced recipe, provide a section titled "이건 어때요?" with suggestions for other related recipes or variations based on the topic, incorporating any unique or creative ideas found in {food_details}(which means, you can recommend other food related to the topic).
                            5. **총 칼로리**:
                                5.1 List the calories for each ingredient in {complete_recipe} and any new ingredients added, directly beside each ingredient (without creating a separate list for calories).
                                5.2 Calculate the total calorie count for the final enhanced recipe.
                                5.3 Present this information clearly at the end of the enhanced recipe.
                            6. **Language: You must use the language of {language} for your answer**.
                            7. ***Remove all the duplicated information (all)***.
                            """},
                                {'role' : 'user', 'content' : complete_recipe},
                                {'role' : 'user', 'content' : language},
                                {'role' : 'user', 'content' : json.dumps(food_details, ensure_ascii=False)}
                            ]
                        )
                        final_answer = completion.choices[0].message.content
                        print(final_answer)
                        while True:
                            continue_question = input('혹시 질문이나 궁금하신 점 있을까요? ')
                            client4 = OpenAI()
                            completion = client4.chat.completions.create(
                                model = 'gpt-4o',
                                messages = [
                                    {'role': 'system', 'content': """
                                    You are a master chef and a helpful assistant. You will receive multiple questions based on {final_answer}.
                                    1. **Answer the Question**
                                    - Provide a thorough and informative response to each question.
                                    2. **Handle Exit Requests**
                                    - If the user's message indicates a desire to leave or end the chat, respond with only the word "quit". Do not add any additional text or commentary.
                                    example:
                                    question no.1 = '아니야 없어', answer = 'quit'
                                    question no.2 = '필요없을 거 같아, answer = 'quit'
                                    question no.3 = '괜찮아', answer = 'quit'
                                    question no.4 = '고마워', answer = 'quit'
                                    question no.5 = '이제 괜찮아, answer = 'quit'
                                    question no.6 = '없어', answer = 'quit'
                                    
                                    3. **Detailed Ingredient Instructions**
                                    - If the user asks how to make specific ***ingredients***, provide a detailed, step-by-step explanation on how to prepare them.
                                    4. **Provide Alternative Recipes**
                                    - If the user requests another recipe related to the current topic or new topic, respond with "(name of the food or recipe)_another_recipe" (including the underscore) without any additional text or commentary.
                                    5. **chat history**
                                    - If user is asking a question regarding previous chat, try to find it in {chat_history}
                                    **Notes:**
                                    - Replace `{final_answer}` with the relevant context or topic as needed.
                                    - Ensure all responses are clear, concise, and relevant to the user's queries.
                                    - Maintain a professional and friendly tone throughout the conversation.
                                    """},
                                    {'role' : 'user', 'content': final_answer},
                                    {'role' : 'user', 'content' : continue_question},
                                ])
                            questions = completion.choices[0].message.content 
                            if questions == 'quit':
                                break
                            elif 'another_recipe' in questions:
                                questions = questions.split('_')[0]
                                another_food_name = questions
                                break
                            else:
                                print(questions)
                                chat_history.append(final_answer)
                                chat_history.append(questions)