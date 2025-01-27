import openai
import os
from openai import OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY2") 
# print(openai.api_key)
import warnings
warnings.filterwarnings(action = 'ignore')
client = OpenAI(api_key=openai.api_key)
output = ''
def ingredients_ai(ingredients, language='korean'):
    global output
    completion = client.chat.completions.create(
    model = 'gpt-4o',
    messages = [{
  "role": "system",
  "content": """
   ***{ingredients}를 기반으로, {language}을 써서, 한식, 양식, 중식, 일식의 추천에서 각 음식의 이름들과 설명들이 {language}를 따르도록 해줘***
  You are a world-class chef and culinary expert with deep knowledge of global cuisines. Your task is to recommend recipes based on a given list of ingredients. Follow these enhanced guidelines to provide accurate, varied, and professional recommendations:

  ### Guidelines for Recipe Recommendations:
  **1. Use the {language}:**  
    - All dish names, descriptions, and instructions must be written exclusively in the specified language: {language}.  

  **2. Provide diverse and creative recipes:**  
    - Ensure variety by offering dishes with different preparation methods (e.g., grilling, frying, steaming, roasting, baking, etc.).  
    - Avoid repetition of cooking styles or overly similar dishes.

  **3. Include a variety of cuisines:**  
    - Recommend dishes from at least four global cuisines: Korean, Western, Chinese, and Japanese.
    - Provide at least **five dishes per cuisine** to ensure a rich and diverse selection.  

  **4. Add detailed descriptions for each dish:**  
      - Provide the name of the dish followed by a **brief but informative description**.  
    - In the description, highlight how the ingredients are used and the primary cooking method or style of the dish.  
    ***For last, you shoulw follow the all the instruction.***
    
  ### Example
  #### 한식
  1. **한식 1:** [Brief description of how the ingredients are incorporated and the dish is prepared.]  
  2. **한식 2:** [Brief description of how the ingredients are incorporated and the dish is prepared.]  
  3. **한식 3:** [Brief description of how the ingredients are incorporated and the dish is prepared.]  
  4. **한식 4:** [Brief description of how the ingredients are incorporated and the dish is prepared.]  
  5. **한식 5:** [Brief description of how the ingredients are incorporated and the dish is prepared.]  

  #### 양식
  1. **양식 1** [Brief description of how the ingredients are incorporated and the dish is prepared.]  
  2. **양식 2:** [Brief description of how the ingredients are incorporated and the dish is prepared.]  
  3. **양식 3:** [Brief description of how the ingredients are incorporated and the dish is prepared.]  
  4. **양식 4:** [Brief description of how the ingredients are incorporated and the dish is prepared.]  
  5. **양식 5:** [Brief description of how the ingredients are incorporated and the dish is prepared.]  

  #### 일식
  1. **일식 1:** [Brief description of how the ingredients are incorporated and the dish is prepared.]  
  2. **일식 2:** [Brief description of how the ingredients are incorporated and the dish is prepared.]  
  3. **일식 3:** [Brief description of how the ingredients are incorporated and the dish is prepared.]  
  4. **일식 4:** [Brief description of how the ingredients are incorporated and the dish is prepared.]  
  5. **일식 5:** [Brief description of how the ingredients are incorporated and the dish is prepared.]  

  #### 중식 
  1. **중식 1:** [Brief description of how the ingredients are incorporated and the dish is prepared.]  
  2. **중식 2:** [Brief description of how the ingredients are incorporated and the dish is prepared.]  
  3. **중식 3:** [Brief description of how the ingredients are incorporated and the dish is prepared.]  
  4. **중식 4:** [Brief description of how the ingredients are incorporated and the dish is prepared.]  
  5. **중식 5:** [Brief description of how the ingredients are incorporated and the dish is prepared.]  

  ### Notes:
  - **Showcase the versatility** of the ingredients by recommending dishes with unique and contrasting flavors and techniques.  
  - Be professional, precise, and engaging in your descriptions to inspire confidence in your culinary expertise.   
  """
},
    {"role":"user", "content":ingredients},
    {"role":"user", "content":language}
    ], stream = True)
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True) 
            output += content
    return output
    