from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.callbacks.manager import CallbackManager
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import re
#----------------------------------------------------------------------
import subprocess
import markdown
import json
import os
import openai
from openai import OpenAI

openai.api_key = os.getenv("OPENAI_API_KEY2") 
# print(openai.api_key)
import warnings
warnings.filterwarnings(action = 'ignore')


#----------------------------------------------------------------------
korea_food = os.path.join(os.path.dirname(__file__), '한식.json')
western_food = os.path.join(os.path.dirname(__file__), '양식.json')
japanses_food = os.path.join(os.path.dirname(__file__), '일식.json')
chinses_food = os.path.join(os.path.dirname(__file__), '중식.json')
embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key)

#----------------------------------------------------------------------
language = '한국어' #추후 변경 가능
def load_documents(country_food):
    if country_food == '한식':
        with open(korea_food, 'r', encoding='utf-8') as k:
            korean_food_list = json.load(k)
        documents = [Document(page_content=filter_text(food_list)) for food_list in korean_food_list]
        return documents
    elif country_food == '양식':
        with open(western_food, 'r', encoding='utf-8') as w:
            western_food_list = json.load(w)
        documents = [Document(page_content=filter_text(food_list)) for food_list in western_food_list]
        return documents
    elif country_food == '일식':
        with open(japanses_food, 'r', encoding='utf-8') as j:
            japanese_food_list = json.load(j)
        documents = [Document(page_content=filter_text(food_list)) for food_list in japanese_food_list]
        return documents
    elif country_food == '중식':
        with open(chinses_food, 'r', encoding='utf-8') as c:
            chinese_food_list = json.load(c)
        documents = [Document(page_content=filter_text(food_list)) for food_list in chinese_food_list]
        return documents
#----------------------------------------------------------------------
# class chat_history:
#     def __init__(self, storage_dir="chat_histories"):
#         self.storage_dir = storage_dir
#         self.user_histories = {}
#         os.makedirs(self.storage_dir, exist_ok=True)

#     def login(self, username):
#         self.username = username
#         self.user_histories[username] = self._load_history(username)

#     def add_message(self, role, content):
#         if not hasattr(self, "username"):
#             raise Exception("로그인이 필요합니다.")
#         self.user_histories[self.username].append({"role": role, "content": content})

#     def get_history(self):
#         if not hasattr(self, "username"):
#             raise Exception("로그인이 필요합니다.")
#         return self.user_histories[self.username]

#     def save_history(self):
#         if not hasattr(self, "username"):
#             raise Exception("로그인이 필요합니다.")
#         filename = os.path.join(self.storage_dir, f"{self.username}_history.json")
#         with open(filename, "w", encoding="utf-8") as file:
#             json.dump(self.user_histories[self.username], file, ensure_ascii=False, indent=4)

#     def _load_history(self, username):
#         filename = os.path.join(self.storage_dir, f"{username}_history.json")
#         if os.path.exists(filename):
#             with open(filename, "r", encoding="utf-8") as file:
#                 return json.load(file)
#         return [] 
#---------------------------------------------------------------------
def filter_text(text):
    text = re.sub(r'\s+', '', text)
    text = re.sub(r'[^a-zA-Z가-힣\s]', '', text)
    text = text.lower()
    return text
query = "Kimbob recipe" #추후 계속 질문을 받는식으로 변경 가능
#----------------------------------------------------------------------
def hybrid_search(query, vector_store, documents, top_k=1):
    # query_embedding = embeddings.embed_query(query)
    vector_result = vector_store.as_retriever().get_relevant_documents(query)
    keyword_result = [doc for doc in documents if query.lower() in doc.page_content.lower()]
    keyword_result = keyword_result[0] if keyword_result else None
    if vector_result:
        final_result = vector_result
    else:
        final_result = keyword_result
    return final_result
#----------------------------------------------------------------------
course = ['한식', '양식', '중식', '일식']
output = ""


# country_food = input('정하세요: ').replace(" ", "_").replace("&", "_")
def recipe_finder(query, country_food=None):
    global output
    current_path = os.getcwd()
    country_food = country_food.replace('"', '')
    country_food = country_food.replace("\"", '')
    if country_food not in course:
        print('다시 선택해 주세요')
    persist_directory=f"{current_path}/chatbot/chroma_{country_food}"
    print(persist_directory)
    if os.path.exists(persist_directory):
        vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings,
        )
        documents = load_documents(country_food)
    callback_handler = StreamingStdOutCallbackHandler()
    callback_manager = CallbackManager([callback_handler])
    llm = ChatOpenAI(model = 'gpt-4o-mini', temperature = 0, streaming=True, callbacks=[callback_handler], api_key=openai.api_key) #streaming=True, callbacks=[callback_handler]
    results = hybrid_search(query, vector_store, documents)
    context = f"""{results} 내용을 바탕으로 질문에 답해 주세요. 질문: {query}
    ***Don't forget to indicate the numbers or weight of the food or ingredients and also indiate the time or weight of the ingredients***
    Example:
    Boil it for 3 minuts -> Must indicate 3 minutes
    Wrong Example
    Boil it and wait -> You must indicate the time in 
    1.1 Identify any additional ingredients, tips, or unique elements that could enhance {results}.
    1.2 Add these enhancements to {results} as suggestions or optional steps, without altering the original recipe structure.(Enhanced Recipe -> 추가 첨가 재료)
    1.3 Provide detailed explanations for each suggestion, including:
        - Specific quantities of new ingredients.
        - Clear steps for incorporating them into the recipe.
        - A brief explanation of how each suggestion improves the dish (max of 4 unique enhancements, no duplicates).
    2. **Output Format**: Present the enhanced recipe in the following structure:
        - Original Recipe: {results}
        - Enhanced Recipe: List the new steps or ingredients clearly as additions to the original.
        - Explanations: Provide detailed explanations for each enhancement (only unique explanations, no repetition).
    3. **Alternative Ideas**:
        4.1 Below the enhanced recipe, provide a section titled "이건 어때요?" with suggestions for other related recipes or variations based on the topic, incorporating any unique or creative ideas found in {results}(which means, you can recommend other food related to the topic).
    4. **총 칼로리**:
        5.1 List the calories for each ingredient in {results}, so don't list the ingredient with calories again. and any new ingredients added, directly beside each ingredient (without creating a separate list for calories).
        5.2 Calculate the total calorie count for the final enhanced recipe.
        5.3 Present this information clearly at the end of the enhanced recipe.
    5. **Language: You must use the language of {results} for your answer**.
    6. ***Remove all the duplicated information (all)***.
        
    Full Example:
    레시피 이름: 고구마튀김 (1인분)
    재료:
    고구마 - 1개 (약 150g, 109 칼로리)
    튀김 가루 - 50g (187 칼로리)
    찬물 - 75ml (0 칼로리)
    식물성 기름 (튀김용) - 적당량 (약 250 칼로리)
    소금 - 약간 (0 칼로리)

    조리 과정:
    1. 고구마 준비:
    - 신선한 고구마를 흐르는 물에 정성스럽게 씻어 흙과 먼지를 완벽히 제거합니다. 고구마 껍질을 벗기면서 자연이 선사한 고운 결을 느껴보세요. 껍질을 벗긴 고구마를 안정된 칼로 약 0.5cm 두께로 얇게 슬라이스합니다. 이때, 일정한 두께로 자르는 것이 고구마의 고른 익힘과 바삭함을 보장합니다.
    2. 튀김 반죽 준비:
    - 작은 볼에 부드럽고 고운 튀김 가루를 담습니다. 여기에 얼음처럼 차가운 물을 부어줍니다. 물은 반죽의 경쾌함을 좌우하므로 충분히 차가워야 합니다. 젓가락이나 거품기를 사용해 부드럽게 반죽을 섞어줍니다. 이때 반죽을 너무 완벽히 섞으려 하지 마세요. 적당히 덩어리가 남아 있어야 튀김의 바삭함을 극대화할 수 있습니다.
    3. 기름 가열:
    - 깊고 넉넉한 냄비나 팬에 식용유를 가득 붓습니다. 기름이 170-180°C에 도달하도록 천천히 가열하며, 이 온도는 고구마가 완벽히 튀겨지는 마법의 순간을 만들어냅니다. 온도를 확인하기 위해 튀김 반죽을 살짝 떨어뜨려 보세요. 반죽이 기름 표면에 닿는 순간 살포시 부풀어 올라 떠오르면 이상적인 온도입니다.
    4. 튀김:
    - 고구마 슬라이스를 반죽에 한 장씩 담급니다. 반죽이 고구마의 모든 면을 섬세하게 감싸도록 조심스럽게 들어 올립니다. 이제, 이 고구마를 뜨겁게 가열된 기름 속으로 부드럽게 밀어 넣습니다. 튀겨지는 고구마가 기름 속에서 춤추듯 움직이며 황금빛으로 변해가는 과정을 지켜보세요. 2-3분 후, 고구마가 노릇하고 바삭한 겉모습으로 변하면 튀김의 향연은 절정을 맞이합니다. 튀겨진 고구마는 키친타월 위에 올려 기름기를 제거합니다.
    5. 마무리 간:
    - 따뜻한 고구마 튀김 위에 소금을 살짝 뿌려줍니다. 소금은 튀김의 자연스러운 단맛을 한층 더 돋보이게 해주는 마지막 터치입니다. 너무 많이 뿌리지 않도록 조심하세요. 소금은 고구마 본연의 맛을 조화롭게 끌어내야 합니다.

    개선 사항:
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

    if you cannot find the documents or recipe in the given folderm, follow the next step
    Don't say anthing but follow the steps below.
    Then follow these steps:
    You are a professional chef who knows every ingredient and detailed cooking process for any dish. When given a specific food topic:
    1. Search and list all essential ingredients for the dish in detail (including quantities if possible).
    2. Provide a step-by-step cooking process with precise instructions and tips for achieving the best results.
    3. Use the language of {language} for your answer.
    4. Do NOT use the example below as the answer to the user's question. It is only a reference for the level of detail expected in your response.
    5.When writing the recipe, ensure to mention the number of servings based on the ingredients provided. Use clear formats such as 'serves 2' or 'serves 4'. 
    6. If the user requests a specific number of servings, such as 1 serving, adjust all the ingredients and steps accordingly and the number of serving will be always 1

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

    Now, provide an equally detailed response for the user's specific name ofthe food: {query}.

    After that you must follow this steps
    1.1 Identify any additional ingredients, tips, or unique elements that could enhance the recipe you made.
    1.2 Add these enhancements to the recipe you made as suggestions or optional steps, without altering the original recipe structure.
    1.3 Provide detailed explanations for each suggestion, including:
        - Specific quantities of new ingredients.
        - Clear steps for incorporating them into the recipe.
        - A brief explanation of how each suggestion improves the dish (max of 4 unique enhancements, no duplicates).
    2. **Output Format**: Present the enhanced recipe in the following structure:
        - Original Recipe: the recipe you made
        - Enhanced Recipe: List the new steps or ingredients clearly as additions to the original.
        - Explanations: Provide detailed explanations for each enhancement (only unique explanations, no repetition).
    3. **Alternative Ideas**:
        4.1 Below the enhanced recipe, provide a section titled "이건 어때요?" with suggestions for other related recipes or variations based on the topic, incorporating any unique or creative ideas found by you(which means, you can recommend other food related to the topic).
    4. **총 칼로리**:
        5.1 List the calories for each ingredient in the recipe you made, so don't list the ingredient with calories again. and any new ingredients added, directly beside each ingredient (without creating a separate list for calories).
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
    개선 사항:
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

    but if you recevied someting like a question, you must follow the instruction below
    You are a master chef and a helpful assistant. You will receive multiple questions based on your answer but don't make any duplicated answers.
    1. **Answer the Question**
    - Provide a thorough and informative response to each question.
    2. **Detailed Ingredient Instructions**
    - If the user asks how to make specific ***ingredients***, provide a detailed, step-by-step explanation on how to prepare them.
    **Notes:**
    - Ensure all responses are clear, concise, and relevant to the user's queries.
    - Maintain a professional and friendly tone throughout the conversation.
    """

    response = llm.invoke(context)
    response = response.content
    return response

def question(response, continue_question):
    chat_history_log = []
    while True:
        continue_question = input('\n혹시 질문이나 궁금하신 점 있을까요? ')
        if continue_question == 'quit':
            break
        client2 = OpenAI(api_key=openai.api_key)
        completion2 = client2.chat.completions.create(
            model = 'gpt-4o-mini',
            messages = [
                {'role': 'system', 'content': """
                You are a master chef and a helpful assistant. You will receive multiple questions based on {response} but don't make any duplicated answers.
                1. **Answer the Question**
                - Provide a thorough and informative response to each question.
                2. **Detailed Ingredient Instructions**
                - If the user asks how to make specific ***ingredients***, provide a detailed, step-by-step explanation on how to prepare them.
                3. **chat history**
                - If user is asking a question regarding previous chat, try to find it in {chat_history_log}
                **Notes:**
                - Replace `{response}` with the relevant context or topic as needed.
                - Ensure all responses are clear, concise, and relevant to the user's queries.
                - Maintain a professional and friendly tone throughout the conversation.
                """},
                {'role' : 'user', 'content': response},
                {'role' : 'user', 'content' : continue_question},
            ], stream= True
            )
        for chunk in completion2:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="", flush = True)
        chat_history_log.append({'role': 'user', 'content': continue_question})
        chat_history_log.append({'role': 'assistant', 'content': completion2})