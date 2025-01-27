# 목차📖
  - [1. 팀 소개](#팀-소개)👥
  - [2. 프로젝트 소개](#프로젝트-소개)🔮
  - [3. 주요 기능 소개](#주요-기능-소개)🎨
  - [4. 기술 스택](#기술-스택)🥽
  - [5. 기술적 의사결정](#기술적-의사결정)⚖️
  - [6. 서비스 아키텍쳐](#6-서비스-아키텍쳐)📶
  - [7. ERD](#7-erd)📊

---
## 팀 소개👥
**팀명: 구.원.조**
| 이름 | 태그 | 역할 |
| --- | --- | --- |
| 전상우 | 리더 | 문서 작성, 배포 |
| 김준기 | 부리더 | 웹 크롤링, Langchain, 프론트엔드|
| 정석훈 | 서기 | 백엔드, Django Restframework, 회의록 작성 |

## 프로젝트 소개🔮
요즘 외식비 부담이 커지면서 집에서 직접 요리하려는 분들이 많아졌습니다. 하지만 요리에 익숙하지 않은 분들을 위해, 한식, 일식, 양식, 중식 레시피를 알려주는 챗봇, **맛.봇**을 기획하게 되었습니다.

단순히 레시피를 제공하는 것만으로는 기존의 레시피 사이트와 차별화가 어렵다는 점이 아쉬웠습니다. 그래서 섭취한 음식을 입력하면 칼로리와 영양분을 분석하고, 사용자에게 맞는 하루 식단을 추천해주는 기능을 추가하기로 했습니다. 이 기능은 사용자의 연령과 다이어트 여부를 반영하며, 입력된 섭취 데이터를 기반으로 최적의 식단을 제안합니다.

**맛봇**은 요리에 자신 없는 초보자뿐만 아니라 건강한 식단 관리를 원하는 분들에게도 유용한 도구가 될 것입니다.

---
## 주요 기능 소개🎨
1. **레시피 제공 기능**: 카테고리를 고른 후, 음식을 입력하여 그 음식의 레시피를 알 수 있습니다.
2. **대체 재료, 추가 재료 제시 기능**: 재료가 부족할 때 대체할 재료나 음식에 추가할 재료를 추천합니다.
3. **사용자가 입력한 데이터를 기반으로 맞춤형 하루 식단 추천**: 사용자가 그 날 섭취한 음식을 분석하여 필요한 영양소와 칼로리에 맞춰 식단을 추천합니다.
4. **사용자의 연령과 체중 감량 여부에 맞춘 레시피 제공**: 사용자의 연령과 체중 감량 여부에 맞춘 식단을 제공합니다
---
## 기술 스택🥽
**백엔드**: Django Rest Framework, python 3.12

**프론트엔드**: Bootstrap

**챗봇**: Langchain, Chroma, OpenAI ChatGPT 4o mini

**데이터베이스**: SQLITE3

**협업 도구**: Slack

**일정 관리**: Notion

---
## 기술적 의사결정⚖️
1. **DRF (Django Rest Framework)**
<details>

    - RESTful API 설계의 간편함: DRF는 Django의 강력한 ORM(Object-Relational Mapping)과 쉽게 통합되어 RESTful API를 간단히 설계할 수 있습니다.

    - 데이터 직렬화: DRF의 `serializers`는 데이터베이스 모델과 JSON 데이터 간의 변환을 단순화하여 데이터 전송을 효율적으로 처리합니다.

    - 확장 가능한 인증 및 권한 시스템: DRF는 다양한 인증 메커니즘(JWT, OAuth 등)을 지원하며, 권한 제어를 쉽게 구현할 수 있습니다.

    - 데이터 직렬화: DRF의 `serializers`는 데이터베이스 모델과 JSON 데이터 간의 변환을 단순화하여 데이터 전송을 효율적으로 처리합니다.

    - 확장 가능한 인증 및 권한 시스템: DRF는 다양한 인증 메커니즘(JWT, OAuth 등)을 지원하며, 권한 제어를 쉽게 구현할 수 있습니다.
</details>

2.  **OpenAI 및 LangChain**
<details>

    - 복잡한 파이프라인 관리: LangChain은 다단계 NLP 워크플로우(예: 크롤링 데이터의 전처리 → GPT 호출 → 결과 후처리)를 쉽게 구성할 수 있는 프레임워크입니다.

    - 모듈화: LangChain은 `CallbackManager`를 통해 워크플로우의 각 단계를 명확히 추적하고 관리할 수 있습니다.

    - LLM 통합: LangChain은 OpenAI뿐만 아니라 Hugging Face와 같은 다양한 LLM을 지원하여 유연한 워크플로우 구성이 가능합니다.(예: 임베딩 모델)
</details>


3. **크롤링 (Selenium + ChromeDriver)**
<details>

    - 동적 웹페이지 처리: Selenium은 JavaScript로 렌더링되는 동적 웹페이지를 크롤링할 수 있습니다.

    - 유연성: Selenium은 다양한 브라우저(Chrome, Firefox 등)를 지원하며, 페이지 상호작용(클릭, 스크롤, 입력 등)을 자동화할 수 있습니다.

    - 확장 가능성: Selenium은 `ChromeDriver`와 같은 브라우저 드라이버를 통해 크롤링 및 자동화 작업을 세밀하게 조정할 수 있습니다.
</details>

4. **Bootstrap**
<details>

    - 반응형 디자인: Bootstrap은 모바일 친화적이고 반응형 웹사이트를 쉽게 제작할 수 있는 CSS 프레임워크입니다.

    - 풍부한 UI 컴포넌트: 버튼, 모달, 카드 등 다양한 사전 설계된 컴포넌트를 제공하여 개발 속도를 높입니다.

    - 사용 용이성: HTML과 CSS에 대한 기본적인 이해만으로도 고급 UI를 설계할 수 있습니다.

    - 풍부한 UI 컴포넌트: 버튼, 모달, 카드 등 다양한 사전 설계된 컴포넌트를 제공하여 개발 속도를 높입니다.

    - 사용 용이성: HTML과 CSS에 대한 기본적인 이해만으로도 고급 UI를 설계할 수 있습니다.
</details>

5. **Python 3.12**
<details>

    - 최신 기능: Python 3.12는 성능 향상 및 새로운 구문적 기능의 사용

    - 광범위한 생태계: Python은 Django, DRF, Selenium, OpenAI, LangChain 등 다양한 라이브러리와의 통합을 지원합니다.
</details>

6. **Chroma**
<details>

    - NLP에 최적화된 벡터 데이터 관리: Chroma는 OpenAI 임베딩 모델로 생성된 데이터를 저장하고 검색할 수 있는 벡터 데이터베이스 기능을 제공합니다.

    - 유연성:  NLP 기반 검색 작업에 필요한 다양한 API와 쉽게 통합됩니다.
</details>

7. **SQLite3**

<details>

    - 경량화: SQLite3는 서버 없이 실행할 수 있는 파일 기반 데이터베이스로, 프로젝트나 로컬 데이터 저장소로 적합합니다.

    - 간편한 관리: SQL 쿼리를 활용하여 크롤링 데이터 및 NLP 결과를 효율적으로 관리할 수 있습니다.

    - 통합성: Python에서 기본 제공되며, Django ORM 및 DRF와 원활히 동작합니다.  
</details> 

---
## 6. 서비스 아키텍쳐📶
![로컬 이미지](Architecture.png)
---
## 7. ERD📊
![로컬 이미지](ERD.png)
---