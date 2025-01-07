from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.callbacks.manager import CallbackManager
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
#----------------------------------------------------------------------
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from sentence_transformers import SentenceTransformer
# from webdriver_manager.chrome import ChromeDriverManager
# import time
#----------------------------------------------------------------------
import requests, json
# from bs4 import BeautifulSoup
import os
import openai
from openai import OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY2")
import warnings
warnings.filterwarnings(action = 'ignore')
import subprocess
#----------------------------------------------------------------------
class chat_history:
    def __init__(self, storage_dir="chat_histories"):
        self.storage_dir = storage_dir
        self.user_histories = {}
        os.makedirs(self.storage_dir, exist_ok=True)

    def login(self, username):
        self.username = username
        self.user_histories[username] = self._load_history(username)

    def add_message(self, role, content):
        if not hasattr(self, "username"):
            raise Exception("로그인이 필요합니다.")
        self.user_histories[self.username].append({"role": role, "content": content})

    def get_history(self):
        if not hasattr(self, "username"):
            raise Exception("로그인이 필요합니다.")
        return self.user_histories[self.username]

    def save_history(self):
        if not hasattr(self, "username"):
            raise Exception("로그인이 필요합니다.")
        filename = os.path.join(self.storage_dir, f"{self.username}_history.json")
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(self.user_histories[self.username], file, ensure_ascii=False, indent=4)

    def _load_history(self, username):
        filename = os.path.join(self.storage_dir, f"{username}_history.json")
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                return json.load(file)
        return [] 
#----------------------------------------------------------------------
# webdriver_options = Options()
# webdriver_options.add_argument("--headless")  
# driver_service = Service(ChromeDriverManager().install()) 
# webdriver_chrome = webdriver.Chrome(service=driver_service, options=webdriver_options)
korea_food = 'C:\\Users\\kevinkim\\Desktop\\recipes\\한식.json'
western_food = 'C:\\Users\\kevinkim\\Desktop\\recipes\\양식.json'
japanses_food = 'C:\\Users\\kevinkim\\Desktop\\recipes\\일식.json'
chinses_food = 'C:\\Users\\kevinkim\\Desktop\\recipes\\중식.json'
embeddings = OpenAIEmbeddings()

course = ['한식', '양식', '중식', '일식']
country_food = input('정하세요: ').replace(" ", "_").replace("&", "_")   
if country_food not in course:
    print('다시 선택해 주세요')
persist_directory=f"chroma_{country_food}"
if os.path.exists(persist_directory):
    vector_store = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
elif country_food == '한식':
    with open(korea_food, 'r', encoding='utf-8') as k:
        korean_food_list = json.load(k)
    documents = [Document(page_content=food_list) for food_list in korean_food_list]
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    vector_store.persist()
elif country_food == '양식':
    with open(korea_food, 'r', encoding='utf-8') as k:
        western_food_list = json.load(k)
    documents = [Document(page_content=food_list) for food_list in western_food_list]
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    vector_store.persist()
    
elif country_food == '일식':
    with open(japanses_food, 'r', encoding='utf-8') as k:
        japanses_food_list = json.load(k)
    documents = [Document(page_content=food_list) for food_list in japanses_food_list]
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    vector_store.persist()
    
elif country_food == '중식':
    with open(korea_food, 'r', encoding='utf-8') as k:
        chinses_food_list = json.load(k)
    documents = [Document(page_content=food_list) for food_list in chinses_food_list]
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    vector_store.persist()
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
llm = ChatOpenAI(model = 'gpt-4o', temperature = 0, streaming=True, callbacks=[StreamingStdOutCallbackHandler()])
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff", 
    retriever=vector_store.as_retriever()
)
query = "고등어찌개 레시피와 칼로리에 대해 설명해주세요." #추후 계속 질문을 받는식으로 변경 가능
response = qa_chain.run(query)  
print(response, end='', flush=True)
# if not response or "죄송" in response:
#     print('외부에서 레시피를 검색하겠습니다! 조금만 기다려주세요!....')
#     subprocess.run(['python', 'search.py'])

chat_history_log = []
while True:
    continue_question = input('혹시 질문이나 궁금하신 점 있을까요? ')
    client = OpenAI()
    completion = client.chat.completions.create(
        model = 'gpt-4o',
        messages = [
            {'role': 'system', 'content': """
            You are a master chef and a helpful assistant. You will receive multiple questions based on {response} but don't make any duplicated answers.
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
            4. **chat history**
            - If user is asking a question regarding previous chat, try to find it in {chat_history_log}
            **Notes:**
            - Replace `{response}` with the relevant context or topic as needed.
            - Ensure all responses are clear, concise, and relevant to the user's queries.
            - Maintain a professional and friendly tone throughout the conversation.
            """},
            {'role' : 'user', 'content': response},
            {'role' : 'user', 'content' : continue_question},
        ] + chat_history_log
        )
    questions = completion.choices[0].message.content 
    if questions.lower() == 'quit':
        print(questions)
        calories = input('칼로리를 확인 후 다음 음식을 추천 받으시겠습니까? y/n')
        if calories == 'y':
            subprocess.run(['python', 'calorie_helper.py'])
        else:
            break
        break
    else:
        print(questions)
        chat_history_log.append({'role': 'user', 'content': continue_question})
        chat_history_log.append({'role': 'assistant', 'content': questions})

