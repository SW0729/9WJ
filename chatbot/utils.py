import os
import json
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()
# OpenAI API 키 설정
import openai
openai.api_key = os.getenv("OPENAI_API_KEY2")  # 환경 변수에서 키 가져오기

if not openai.api_key:
    raise ValueError("OpenAI API 키가 설정되지 않았습니다. 환경 변수를 확인하세요.")

def load_kjk_data(json_path, food_type):
    """
    JSON 파일과 요리 종류를 받아 데이터를 Chroma 데이터베이스에 저장.
    """
    # Chroma 데이터베이스 저장 경로
    persist_directory = os.path.join(os.path.dirname(__file__), f"chroma_{food_type}")

    # Embeddings 객체 생성
    embeddings = OpenAIEmbeddings()

    # JSON 파일 로드
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            food_data = json.load(f)
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {json_path}")
        return

    # Document 객체 생성
    documents = [Document(page_content=item) for item in food_data]

    # Chroma 데이터베이스 업데이트 또는 생성
    if os.path.exists(persist_directory):
        vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings,
        )
        vector_store.add_documents(documents)
        vector_store.persist()
        print(f"{food_type} 데이터가 기존 Chroma 데이터베이스에 추가되었습니다.")
    else:
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory=persist_directory,
        )
        vector_store.persist()
        print(f"{food_type} 데이터로 새 Chroma 데이터베이스가 생성되었습니다.")
