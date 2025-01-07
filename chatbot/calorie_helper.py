from KJK_data_collect import query, response
import os
import openai
from openai import OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY2")
from PyPDF2 import PdfReader
import re

pdf_path = 'C:\\Users\\kevinkim\\Desktop\\Daily Calories\\Daily recommended Calories.pdf' #추후 변경 가능
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
recommendation_history = []
while True:
    if chosen_language == 'Korean':
        time_check = input(f'''안녕하세요! 저는 당신의 식단을 책임질 SpartaChef입니다! 
            이미 식사를 하셨나요? 혹시 언제 혹은 몇시에 드실 예정인지 알 수 있을까요?
            예: 아침 6시, 오후 2시 등: ''')
    else:  
        time_check = (f'''Hello! I am SpartaChef, your diet assistant! 
            Have you already finished your dish?. Can you tell me when you ate or when are you planning to eat?
            Example: 6 AM, 2 PM, etc.: ''')
    client = OpenAI()
    completion = client.chat.completions.create(
        model = 'gpt-4o',
        messages = [
        {'role':'system', 'content': """
        You are a helpful assistant named SpartaChef who helps people with their menu({query}, remember you must only to take the name of the dish)
        Start by trying to figure out the time the user ate that food (you can round the minutes: for example, 6:48 am = 7 am).
        The time: {time_check}
        Example:
        morning (Typically from 6:00 AM to 12:00 PM).
        afternoon (From 12:00 PM to around 6:00 PM).
        evening (From 6:00 PM to 9:00 PM).
        
        If the user mentions the time, answer in the following format:
        morning: 8 am
        afternoon: 3 pm
        evening: 8 pm
        
        If the user is not typing a valid time or anything unrelated, respond with "none" and never say something else but none. 
        Do not say anything else when you say "none".
        Always follow the language set in the prompt (e.g., if the language is Korean, respond in Korean).
        """},
        {'role':'user', 'content' : chosen_language},
        {'role':'user', 'content' : query},
        {'role':'user', 'content' : time_check},
        
    ])
    time_menu = completion.choices[0].message.content
    if time_menu == 'none':
        print('잘모르겠어요....다시 말씀해 주실 수 있나요?')
        continue
    client1 = OpenAI()
    completion = client1.chat.completions.create(
        model='gpt-4o',
        messages=[
            {'role': 'system', 'content': """
            You are a professional Personalized Nutrition Specialist and Nutrition Data Analyst. Follow these instructions carefully:
            
            1. **Analyze the Nutrients:**
            - Analyze the nutrients and calorie content of the food and its ingredients based on {response}.
            - Predict the calories and nutrients (e.g., proteins, carbs, fats, vitamins, etc.) of the given recipe.
            - Identify any nutritional deficiencies or excesses using {nutrition_file}, considering the time of day ({food_time}).
            - Always respond in the language specified by {chosen_language}.
            
            2. **Recommend Food:**
            - Based on the user's meal time ({time_menu}), recommend appropriate food or menu options for the upcoming meals (until the next day).
            - Recommendations should align with the calculated calorie and nutrient needs.
            - Consider the user's cultural and language preferences based on {chosen_language}.
            
            - **Morning:** If the user ate in the morning, recommend menus for lunch and dinner.
            - **Lunch:** If the user ate at lunch, recommend a menu for dinner.
            - **Dinner:** If the user ate at dinner, recommend a menu for the next day's breakfast.
            """
            },
            {'role': 'user', 'content': response},
            {'role': 'user', 'content': chosen_language},
            {'role': 'user', 'content': time_menu},
        ])
    recommendation = completion.choices[0].message.content
    print(recommendation)
    while True:
        continue_question = input('혹시 질문이나 궁금하신 점 있을까요? ')
        client4 = OpenAI()
        completion = client4.chat.completions.create(
            model='gpt-4o',
            messages=[
                {'role': 'system', 'content': """
                You are a master chef and a helpful health trainer. You will receive multiple questions based on {recommendation} but don't make any duplicated answers.
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
            
                3. **Detailed Instructions**
                - If the user asks how to make specific ***ingredients***, provide a detailed, step-by-step explanation on how to prepare them.
                4. **chat history**
                - If user is asking a question regarding previous chat, try to find it in {chat_history}
                **Notes:**
                - Ensure all responses are clear, concise, and relevant to the user's queries.
                - Maintain a professional and friendly tone throughout the conversation.
                """},
                {'role': 'user', 'content': final_answer},
                {'role': 'user', 'content': continue_question},
            ])
        menu_questions = completion.choices[0].message.content
        if menu_questions == 'quit':
            print(menu_questions)
            break
        else:
            print(menu_questions)
            recommendation_history.append(recommendation)
            recommendation_history.append(menu_questions)
