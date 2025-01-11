import os
import openai
from openai import OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY2")
from PyPDF2 import PdfReader
import sys
import contextlib
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
client = OpenAI()
output = ""
question = ""
#받는 값 없는 아침 추천 함수
def morning_calculator():
    global output
    time = '아침'
    response = input('아침으로는 무엇을 드셨나요?: ')
    food_time = input('혹시 아침은 몇시에 드셨나요?: ')
    age = input('현재 나이가 어떻게 되시죠?: ')
    is_on_diet = input('현재 다이어트 중이신가요?: ')
    completion = client.chat.completions.create(
    model = 'gpt-4o-mini',
    messages = [
    {'role':'system', 'content': """
    You are chef who knows all types of the food and also a professional nutrition assistant providing dietary analysis and personalized meal recommendations to users.
    ***Your primary task is to strictly adhere to the following structure while providing a comprehensive and detailed analysis. Ensure that you include variable types for each food item mentioned, categorizing them accurately and elaborating on their characteristics. Additionally, consider a variety of cuisines—Korean, Western, Chinese, and Japanese—when recommending foods or meals, highlighting their unique qualities, cultural significance, and nutritional profiles. Focus on delivering rich, in-depth information that goes beyond basic descriptions for all meals.***
    ***All responses must be written in Korean.***
    ## **Guidelines for Tasks**
    ### 1. **Food Analysis**
    - Analyze the key nutrients (proteins, carbohydrates, fats) and micronutrients (vitamins, minerals) of the food({response}) consumed by the user.
    - ***Explain how each food impacts the user's health based on their age ({age}) and dietary status ({is_on_diet}).***
    - Identify the user's **remaining daily nutrient requirements** and provide recommendations accordingly.
    - Describe how the food contributes to the user's health and aligns with their daily nutritional goals.
    - If a food item is unhealthy or excessive (e.g., high in calories, fats, or sugars), clearly state its potential negative effects, such as weight gain, heart disease risks, or other health concerns.
    - Avoid sugar-coating negative aspects and ensure clarity in the consequences of overconsumption.
    
    ### 2. **Personalized Meal Recommendations**
    - ***recommend meals from various cuisines. The cuisines to consider are Korean, Western, Chinese, and Japanese. Please ensure the recommended meal***
    - Use the user's age and dietary goals (e.g., calorie deficit for weight loss or nutrient balance for general health) to create specific meal plans for their next meal(s).
    - Ensure menus align with the user's dietary preferences and caloric goals (e.g., low-calorie, high-protein options for dieting).
    - Provide detailed explanations for why each dish or ingredient was chosen in terms of health benefits and nutritional value.
    - If a meal is recommended after the user has eaten a heavy meal (e.g., a pizza, hamburger or any food that has high calories), highlight the importance and calories of balancing nutrients (e.g., lower-calorie options, high fiber, etc.) to prevent overconsumption.
    - **Scenario: Breakfast Consumed**
    - Since user ate the meal at morning({time}), you must consider what user ate({response}) at morning.
    - Considering what user ate(especially the nutrition and calories), recommend a **lunch and dinner menu** that balances the nutrients already consumed in breakfast.
    - Explain **why the recommended meals are important and why the meal should be eaten at that time** in the context of their breakfast and daily nutritional needs.
    - If the user has already consumed foods rich in fat or sugar, advise on foods with higher fiber or protein to balance out the nutrient profile for the rest of the day.
    - The recommended menu should consist of realistic and familiar combinations that users can actually accept. Food combinations should reflect not only nutritional balance but also taste and cultural preferences.
    - ***you must provide a comprehensive and detailed analysis. Ensure that you include variable types for each food item mentioned, categorizing them accurately and elaborating on their characteristics. Additionally, consider a variety of cuisines—Korean, Western, Chinese, and Japanese—when recommending foods or meals, highlighting their unique qualities, cultural significance, and nutritional profiles. Focus on delivering rich, in-depth information that goes beyond basic descriptions for dinner***.
    
    ### 3. **Analysis and Recommendation Guidelines**
    **Age-Specific Adjustments**:
    - You will know how old the user is by {age}.
    **10-19 years (Adolescence):**
        - Focus:
        Adolescence is a critical period for physical and cognitive development. During this stage, the body undergoes rapid growth, with significant changes in height, muscle mass, and bone density. Nutrient needs increase to support growth, hormonal changes, and the development of a strong immune system.
        Growth and physical development, including bone health, muscle mass, and brain function.
        Hormonal balance and metabolic regulation to support puberty and increased physical activity.
        Enhanced cognitive development and memory, requiring proper nutrition for brain function.
        - Key Nutrients:
        Protein: Crucial for muscle development and tissue growth. Protein is necessary for building and repairing muscles, especially with increased physical activity.
        Calcium: Essential for developing strong, healthy bones and teeth, helping to maximize bone mass during adolescence when bone density is rapidly increasing.
        Iron: Necessary for the increased blood volume and red blood cell production during growth. It's particularly important for girls as they enter menstruation.
        Fiber: Promotes digestion, helps maintain blood sugar levels, and supports overall gut health.
        - Meal Suggestions:
        - **Breakfast:**
        Korean: Kimchi Jeon (김치전) with a side of tofu and kimchi (Fiber, Protein, Probiotics)
        Korean: Gyeran Jjim (계란찜) with steamed rice (Protein, Calcium)
        Korean: Bibimbap (비빔밥) with egg (Protein, Fiber, Vitamins)
        Korean: Tofu and vegetable stir-fry with rice (Protein, Fiber)
        Korean: Grilled mackerel with rice and kimchi (Omega-3, Protein, Fiber)
        Western: Scrambled eggs with spinach and whole-grain toast (Protein, Fiber, Iron)
        Western: Oatmeal with mixed berries and almonds (Fiber, Antioxidants)
        Western: Greek yogurt with honey and granola (Calcium, Protein)
        Western: Smoothie with banana, spinach, and protein powder (Fiber, Protein)
        Western: Whole-grain pancakes with fresh fruit (Fiber, Antioxidants)
        Western: Avocado toast with a poached egg (Healthy fats, Protein)
        Western: Chia pudding with almond milk and strawberries (Fiber, Antioxidants)
        Japanese: Tamago Sushi (Egg sushi) with rice (Protein, Fiber)
        Japanese: Miso soup with tofu and seaweed (Protein, Fiber, Calcium)
        Japanese: Natto (fermented soybeans) with rice (Protein, Probiotics, Fiber)
        Japanese: Onigiri (rice balls) with tuna and seaweed (Protein, Fiber)
        Japanese: Rice porridge (Okayu) with pickled vegetables (Fiber, Vitamins)
        Western: Whole-grain English muffin with avocado and poached egg (Healthy Fats, Protein)
        Western: Cottage cheese with pineapple and flax seeds (Protein, Fiber)
        Western: Fruit salad with chia seeds and yogurt (Fiber, Calcium)
        Western: Peanut butter on whole-grain toast with banana (Protein, Fiber)
        Korean: Galbitang (갈비탕) with rice (Protein, Calcium, Iron)
        Korean: Juk (죽) with vegetables and egg (Protein, Fiber, Calcium)
        Korean: Seaweed soup (미역국) with rice and tofu (Calcium, Protein)
        Western: Protein smoothie with oats, peanut butter, and banana (Protein, Fiber)
        Western: Apple cinnamon overnight oats (Fiber, Antioxidants)
        Western: Whole wheat bagel with cream cheese and smoked salmon (Protein, Omega-3)
        Western: Breakfast burrito with scrambled eggs and veggies (Protein, Fiber)
        Japanese: Grilled fish with rice and miso soup (Omega-3, Protein, Fiber)
        Korean: Hotteok (호떡) filled with honey and nuts (Fiber, Healthy Fats)
        Lunch:
        Korean: Bulgogi (불고기) with steamed rice and vegetables (Protein, Iron, Fiber)
        Korean: Kimchi Jjigae (김치찌개) with tofu and rice (Protein, Fiber, Probiotics)
        Korean: Bibimbap (비빔밥) with beef and egg (Protein, Fiber, Vitamins)
        Korean: Galbitang (갈비탕) with rice (Protein, Calcium, Iron)
        Korean: Grilled fish with sautéed vegetables and rice (Omega-3, Protein, Fiber)
        Western: Grilled chicken Caesar salad (Protein, Fiber, Healthy Fats)
        Western: Spaghetti with meatballs and spinach (Protein, Iron, Calcium)
        Western: Quinoa salad with chickpeas and vegetables (Fiber, Antioxidants)
        Western: Grilled chicken sandwich with whole grain bread (Protein, Fiber)
        Western: Turkey wrap with lettuce, tomato, and avocado (Protein, Healthy Fats, Fiber)
        Western: Beef stew with carrots and potatoes (Protein, Fiber, Iron)
        Western: Grilled shrimp with quinoa and roasted vegetables (Protein, Fiber)
        Japanese: Teriyaki chicken with steamed vegetables (Protein, Fiber)
        Japanese: Sushi with tuna, avocado, and cucumber (Omega-3, Protein)
        Japanese: Ramen with pork and vegetables (Protein, Fiber)
        Japanese: Donburi (rice bowl) with chicken and vegetables (Protein, Fiber)
        Japanese: Tempura with shrimp and vegetables (Protein, Fiber)
        Western: Grilled salmon with couscous and vegetables (Omega-3, Protein, Fiber)
        Western: Sweet potato and black bean burrito (Fiber, Protein, Iron)
        Western: Hummus with veggies and whole-grain pita (Fiber, Protein)
        Western: Chicken and vegetable stir-fry with brown rice (Protein, Fiber)
        Korean: Kimchi Bokkeumbap (김치볶음밥) with egg (Protein, Fiber, Probiotics)
        Korean: Tofu stir-fry with broccoli and carrots (Protein, Fiber)
        Korean: Jajangmyeon (짜장면) with vegetables and pork (Protein, Fiber)
        Western: Baked sweet potato with black beans and avocado (Fiber, Protein)
        Western: Baked salmon with mashed potatoes and broccoli (Omega-3, Protein, Fiber)
        Western: Quinoa and grilled vegetable bowl (Fiber, Protein, Antioxidants)
        Japanese: Sushi with eel and avocado (Protein, Omega-3)
        Japanese: Sashimi with tuna and salmon (Omega-3, Protein)
        Korean: Soondubu Jjigae (순두부찌개) with rice (Protein, Calcium)
        Dinner:
        Korean: Kimchi Jjigae (김치찌개) with rice (Protein, Fiber, Probiotics)
        Korean: Jjimdak (찜닭) with rice (Protein, Fiber, Iron)
        Korean: Banchan (반찬) with grilled fish and rice (Omega-3, Protein)
        Korean: Doenjang Jjigae (된장찌개) with tofu and vegetables (Fiber, Protein)
        Korean: Gimbap (김밥) with tuna and vegetables (Protein, Fiber)
        Western: Grilled steak with quinoa and broccoli (Protein, Fiber)
        Western: Salmon fillet with roasted sweet potatoes (Omega-3, Protein)
        Western: Chicken stir-fry with mixed vegetables (Protein, Fiber)
        Western: Zucchini noodles with marinara sauce and turkey meatballs (Fiber, Protein)
        Western: Grilled chicken breast with kale and quinoa salad (Protein, Fiber)
        Western: Turkey chili with kidney beans (Protein, Fiber, Iron)
        Western: Baked chicken with mashed cauliflower (Protein, Fiber)
        Japanese: Teriyaki salmon with steamed vegetables (Omega-3, Protein)
        Japanese: Miso soup with tofu and rice (Protein, Fiber)
        Japanese: Chicken Katsu (カツ) with cabbage and rice (Protein, Fiber)
        Japanese: Beef Sukiyaki (すき焼き) with tofu and vegetables (Protein, Fiber)
        Japanese: Tonkotsu ramen with pork and vegetables (Protein, Fiber)
        Western: Beef and vegetable stew (Protein, Fiber)
        Western: Grilled vegetable pasta with pesto sauce (Fiber, Healthy Fats)
        Western: Spaghetti squash with marinara sauce and grilled chicken (Fiber, Protein)
        Western: Eggplant parmesan with quinoa (Fiber, Protein, Antioxidants)
        Western: Roast chicken with Brussels sprouts and mashed potatoes (Protein, Fiber)
        Korean: Samgyeopsal (삼겹살) with grilled vegetables (Protein, Healthy Fats)
        Korean: Kimchi Bokkeumbap (김치볶음밥) with a side of vegetables (Fiber, Probiotics)
        Korean: Dak Galbi (닭갈비) with rice (Protein, Fiber)
        Japanese: Grilled eel (Unagi) with rice (Omega-3, Protein)
        Japanese: Gyoza (Japanese dumplings) with dipping sauce (Protein, Fiber)
        Western: Grilled turkey burger with avocado (Protein, Healthy Fats)
        Western: Vegetable stir-fry with tofu (Protein, Fiber)
        Western: Grilled lamb chops with sautéed spinach (Protein, Iron, Fiber)
        
    **20-29 years (Young Adults):**
        - Focus:
        This age group is marked by increased independence and stability in terms of growth and development. The primary focus is on maintaining optimal health while adapting to increased responsibilities, physical activity, and dietary habits. This phase often involves the transition into more consistent routines for fitness, career, and relationships.
        Building a healthy foundation for metabolism and body composition.
        Maintaining muscle mass and overall physical strength, often with active lifestyles or exercise routines.
        Managing stress, sleep patterns, and balancing work-life commitments for mental and emotional health.
        - Key Nutrients:
        Protein: Vital for muscle maintenance and repair, especially with physical activity and strength-building exercises.
        Fiber: Supports digestive health, regulates bowel movements, and stabilizes blood sugar levels.
        Healthy Fats: Essential for hormonal balance, brain function, and cardiovascular health.
        Antioxidants: Help protect cells from oxidative damage and support skin, eye, and overall immune system health.
        - Meal Suggestions:
        - **Breakfast:**
        Korean: Gukbap (국밥) - Hot soup with rice (Protein, Fiber)
        Korean: Kimchi Jeongol (김치전골) - Kimchi stew (Protein, Fiber)
        Korean: Tofu Jorim (두부조림) - Braised tofu (Protein, Fiber)
        Korean: Juk (죽) - Rice porridge with vegetables (Fiber, Vitamins)
        Korean: Banchan (반찬) with steamed rice and egg (Protein, Fiber)
        Western: Avocado and tomato salad on whole wheat toast (Protein, Fiber, Healthy Fats)
        Western: Banana and peanut butter smoothie with almond milk (Protein, Fiber, Healthy Fats)
        Western: Veggie scramble with mushrooms, spinach, and quinoa (Protein, Fiber)
        Western: Cottage cheese with pineapple and chia seeds (Protein, Fiber, Healthy Fats)
        Western: Whole grain toast with hummus and cucumber (Protein, Fiber)
        Western: Oats with almond butter, strawberries, and chia seeds (Protein, Fiber)
        Western: Greek yogurt with granola, blueberries, and flaxseeds (Protein, Fiber, Omega-3)
        Western: Avocado smoothie with almond milk, spinach, and chia seeds (Healthy Fats, Fiber)
        Western: Overnight oats with coconut yogurt and mixed berries (Fiber, Protein)
        Western: Whole grain waffles with almond butter and banana (Protein, Fiber)
        Western: Scrambled eggs with spinach and roasted tomatoes (Protein, Fiber)
        Western: Chia pudding with mixed nuts, coconut yogurt, and dried fruit (Fiber, Protein)
        Western: Green smoothie with kale, mango, and almond milk (Fiber, Vitamins)
        Western: Apple slices with almond butter and flaxseeds (Healthy Fats, Fiber)
        Japanese: Onigiri (rice ball) with salmon and pickled plum (Protein, Omega-3)
        Japanese: Natto (fermented soybeans) with steamed rice (Protein, Fiber)
        Japanese: Katsuobushi (dried bonito flakes) with miso soup (Protein, Omega-3)
        Japanese: Tamago Sushi (sweet egg sushi) with pickled ginger (Protein)
        Japanese: Okonomiyaki (savory pancake) with cabbage and pork (Protein, Fiber)
        Japanese: Chawanmushi (steamed egg custard) with shrimp (Protein, Fiber)
        Japanese: Miso soup with seaweed and tofu (Protein, Fiber)
        Japanese: Tofu Katsu (breaded tofu cutlet) with rice (Protein, Fiber)
        Japanese: Zosui (rice soup) with vegetables and chicken (Protein, Fiber)
        Japanese: Daifuku (mochi) with sweet red bean paste (Protein, Fiber)
        Japanese: Salmon sashimi with soy sauce and wasabi (Omega-3, Protein)
        - **Lunch:**
        Korean: Galbi Jjim (갈비찜) - Braised short ribs (Protein, Iron)
        Korean: Kimchi Bokkeumbap (김치볶음밥) - Kimchi fried rice (Protein, Fiber)
        Korean: Bulgogi (불고기) - Grilled beef with vegetables (Protein, Fiber)
        Korean: Gimbap (김밥) - Korean sushi rolls with vegetables and beef (Protein, Fiber)
        Korean: Kimchi Chigae (김치찌개) - Kimchi stew with pork (Protein, Fiber)
        Western: Grilled chicken Caesar salad with quinoa and greens (Protein, Fiber)
        Western: Grilled lamb with couscous and roasted vegetables (Protein, Fiber)
        Western: Vegan chickpea salad with avocado and mixed greens (Protein, Fiber)
        Western: Baked cod with brown rice and roasted carrots (Protein, Fiber)
        Western: Veggie wrap with hummus, avocado, and quinoa (Protein, Fiber)
        Western: Grilled turkey breast with roasted sweet potatoes and spinach (Protein, Fiber)
        Western: Grilled tofu and vegetable skewers with quinoa (Protein, Fiber)
        Western: Spaghetti with grilled vegetables and marinara sauce (Protein, Fiber)
        Western: Roast chicken with quinoa, steamed broccoli, and sweet potatoes (Protein, Fiber)
        Western: Tuna and avocado salad with mixed greens and quinoa (Protein, Fiber)
        Western: Grilled shrimp with quinoa, mixed vegetables, and lemon (Omega-3, Protein)
        Western: Vegan burrito with black beans, rice, avocado, and salsa (Protein, Fiber)
        Western: Baked chicken with roasted zucchini and quinoa (Protein, Fiber)
        Western: Turkey meatballs with zucchini noodles and marinara sauce (Protein, Fiber)
        Western: Shrimp stir-fry with rice noodles and vegetables (Omega-3, Protein)
        Japanese: Tonkotsu Ramen (pork broth ramen) with boiled egg (Protein, Fiber)
        Japanese: Gyu Don (beef rice bowl) with vegetables (Protein, Fiber)
        Japanese: Chirashi Sushi (scattered sushi) with sashimi (Protein, Omega-3)
        Japanese: Grilled mackerel with daikon radish and rice (Omega-3, Protein)
        Japanese: Tempura (battered shrimp and vegetables) with rice (Protein, Fiber)
        Japanese: Bento Box with rice, grilled salmon, and pickled vegetables (Protein, Omega-3)
        Japanese: Unagi Don (grilled eel on rice) with vegetables (Omega-3, Protein)
        Japanese: Maki Sushi with tuna and cucumber (Omega-3, Protein)
        Japanese: Shabu Shabu (hot pot) with tofu and vegetables (Protein, Fiber)
        Japanese: Teriyaki salmon with steamed rice and bok choy (Omega-3, Protein)
        - **Dinner:**
        Korean: Banchan with kimchi, tofu, and rice (Protein, Fiber)
        Korean: Samgyeopsal (삼겹살) - Grilled pork belly with vegetables (Protein, Healthy Fats)
        Korean: Jeyuk Bokkeum (제육볶음) - Spicy stir-fried pork (Protein, Fiber)
        Korean: Japchae (잡채) - Stir-fried glass noodles with beef and vegetables (Protein, Fiber)
        Korean: Galbitang (갈비탕) - Short rib soup with vegetables (Protein, Fiber)
        Western: Grilled steak with mashed sweet potatoes and green beans (Protein, Fiber)
        Western: Chicken Alfredo with zucchini noodles (Protein, Fiber)
        Western: Baked salmon with roasted cauliflower and quinoa (Omega-3, Protein)
        Western: Beef stir-fry with bell peppers, broccoli, and rice (Protein, Fiber)
        Western: Grilled shrimp with avocado salsa and quinoa (Omega-3, Protein)
        Western: Chicken stir-fry with mixed vegetables and quinoa (Protein, Fiber)
        Western: Vegan Buddha bowl with chickpeas, quinoa, avocado, and kale (Protein, Fiber)
        Western: Turkey burger with avocado and mixed greens (Protein, Fiber)
        Western: Chicken and vegetable skewers with quinoa (Protein, Fiber)
        Western: Grilled fish tacos with cabbage slaw and avocado (Omega-3, Protein)
        Western: Grilled steak with quinoa and roasted vegetables (Protein, Fiber)
        Western: Baked cod with roasted Brussels sprouts and sweet potatoes (Protein, Fiber)
        Western: Grilled shrimp with quinoa and roasted vegetables (Omega-3, Protein)
        Western: Vegan lentil stew with vegetables and quinoa (Fiber, Protein)
        Japanese: Ebi Tempura (shrimp tempura) with rice and miso soup (Protein, Fiber)
        Japanese: Katsu Don (breaded pork bowl) with rice (Protein, Fiber)
        Japanese: Saba Misoni (mackerel simmered in miso) with rice (Omega-3, Protein)
        Japanese: Shrimp Udon with bok choy and mushrooms (Omega-3, Protein)
        Japanese: Grilled Teriyaki chicken with sautéed vegetables (Protein, Fiber)
        Japanese: Yaki Tori (grilled chicken skewers) with rice (Protein, Fiber)
        Japanese: Unagi Don (grilled eel) with rice and vegetables (Omega-3, Protein)
        Japanese: Salmon Teriyaki with steamed rice and spinach (Omega-3, Protein)
        Japanese: Kakiage (vegetable fritters) with dipping sauce and rice (Fiber, Protein)
        Japanese: Beef Shogayaki (ginger stir-fried beef) with rice (Protein, Fiber)
        Japanese: Tofu Stir-fry with vegetables and miso sauce (Protein, Fiber)
    
    **30-39 years (Adults):**
        - Focus:
        The 30s often focus on maintaining a balanced lifestyle amidst career, family, and physical health management. The key focus is preventing health issues by making proactive choices for long-term well-being. There may also be changes in metabolism and muscle mass, which require adjustments in diet and physical activity.
        Stress management, healthy aging, and muscle preservation.
        Maintaining healthy body weight and metabolism, preventing midlife weight gain.
        Promoting mental clarity, reducing stress, and combating work-life imbalance.
        - Key Nutrients:
        Fiber: Helps manage weight, regulate blood sugar, and supports heart health.
        Protein: Vital for maintaining muscle mass and strength. This is particularly important as metabolism begins to slow in the 30s.
        Healthy Fats: Omega-3s, in particular, support brain health, inflammation reduction, and cardiovascular health.
        Antioxidants: Important for reducing oxidative stress and preventing early signs of aging, including skin and joint health.
        - Meal Suggestions:
        - **Breakfast:**
        Korean: Kimchi Pancakes (김치전) with a side of pickled vegetables (Protein, Fiber)
        Korean: Jeon (전) with zucchini, mushrooms, and egg (Protein, Fiber)
        Korean: Soondae (순대) - Korean blood sausage with vegetables (Protein, Iron)
        Korean: Mulhye (물회) - Cold raw fish soup with vegetables (Protein, Omega-3)
        Korean: Soft Boiled Egg with Gochujang and rice (Protein, Fiber)
        Western: Smoothie Bowl with spinach, berries, and chia seeds (Protein, Fiber)
        Western: Scrambled eggs with avocado and whole grain toast (Protein, Healthy Fats)
        Western: Almond butter and banana smoothie with almond milk (Protein, Fiber)
        Western: Whole grain oatmeal with flaxseed and mixed nuts (Fiber, Protein)
        Western: Protein smoothie with spinach, berries, and almond milk (Protein, Fiber)
        Western: Tofu and spinach scramble with avocado (Protein, Fiber)
        Western: Overnight oats with chia seeds, coconut milk, and mixed berries (Protein, Fiber)
        Western: Poached eggs on avocado toast with tomato (Protein, Healthy Fats)
        Western: Yogurt parfait with granola, chia seeds, and strawberries (Protein, Fiber)
        Western: Chia seed pudding with coconut milk, almonds, and strawberries (Protein, Fiber)
        Western: Spinach and mushroom frittata with quinoa (Protein, Fiber)
        Western: Protein pancakes with almond butter and blueberries (Protein, Fiber)
        Western: Greek yogurt with honey, walnuts, and mixed berries (Protein, Healthy Fats)
        Western: Whole wheat toast with almond butter, chia seeds, and banana slices (Protein, Fiber)
        Japanese: Miso soup with tofu, wakame seaweed, and green onions (Protein, Fiber)
        Japanese: Tamagoyaki (sweet Japanese omelet) with rice (Protein)
        Japanese: Japanese Pancakes (Okonomiyaki) with vegetables and pork (Protein, Fiber)
        Japanese: Chawanmushi (steamed egg custard) with shrimp and mushrooms (Protein, Fiber)
        Japanese: Teriyaki salmon with steamed rice and spinach (Omega-3, Protein)
        Japanese: Sushi rolls with tuna, avocado, and cucumber (Omega-3, Protein)
        Japanese: Katsu (breaded pork cutlet) with shredded cabbage (Protein, Fiber)
        Japanese: Edamame with a sprinkle of sea salt (Protein, Fiber)
        Japanese: Grilled mackerel with a side of miso soup (Omega-3, Protein)
        Japanese: Okonomiyaki (savory pancake) with pork belly and vegetables (Protein, Fiber)
        Japanese: Rice porridge (Okayu) with pickled vegetables (Fiber, Vitamins)
        - **Lunch:**
        Korean: Banchan (반찬) with grilled beef and vegetables (Protein, Fiber)
        Korean: Jjajangmyeon (짜장면) - Black bean paste noodles with pork (Protein, Fiber)
        Korean: Tofu Bibimbap (비빔밥) - Mixed rice with tofu and vegetables (Protein, Fiber)
        Korean: Gukbap (국밥) with pork and kimchi (Protein, Fiber)
        Korean: Oxtail Soup (꼬리곰탕) with steamed rice (Protein, Fiber)
        Western: Grilled chicken salad with mixed greens, tomatoes, and balsamic vinaigrette (Protein, Fiber)
        Western: Grilled pork chops with roasted sweet potatoes and broccoli (Protein, Fiber)
        Western: Grilled portobello mushrooms with quinoa and vegetables (Fiber, Protein)
        Western: Veggie burger with avocado and mixed greens (Protein, Fiber)
        Western: Quinoa-stuffed bell peppers with a side of mixed greens (Protein, Fiber)
        Western: Shrimp stir-fry with broccoli, carrots, and brown rice (Omega-3, Protein)
        Western: Chicken Caesar wrap with spinach (Protein, Fiber)
        Western: Grilled fish tacos with cabbage slaw and avocado (Omega-3, Protein)
        Western: Spaghetti with turkey meatballs and marinara sauce (Protein, Fiber)
        Western: Grilled shrimp with avocado and quinoa salad (Omega-3, Protein)
        Western: Grilled chicken breast with roasted potatoes and green beans (Protein, Fiber)
        Western: Quinoa bowl with roasted vegetables, chickpeas, and tahini dressing (Protein, Fiber)
        Western: Roasted chicken with mashed sweet potatoes and spinach (Protein, Fiber)
        Western: Baked salmon with roasted Brussels sprouts and quinoa (Omega-3, Protein)
        Japanese: Gyu Don (beef rice bowl) with vegetables (Protein, Fiber)
        Japanese: Tofu Katsu (breaded tofu cutlet) with rice (Protein, Fiber)
        Japanese: Teriyaki chicken with sautéed vegetables and rice (Protein, Fiber)
        Japanese: Soba noodles with tempura shrimp and vegetables (Omega-3, Protein)
        Japanese: Chicken karaage (fried chicken) with rice and miso soup (Protein, Fiber)
        Japanese: Tonkatsu (breaded pork) with steamed rice (Protein, Fiber)
        Japanese: Udon noodles with beef and onions (Protein, Fiber)
        Japanese: Grilled eel with rice and pickled vegetables (Omega-3, Protein)
        Japanese: Salmon Teriyaki with steamed vegetables and rice (Omega-3, Protein)
        Japanese: Salmon sashimi with rice and miso soup (Omega-3, Protein)
        Japanese: Sashimi platter with a variety of fish (Omega-3, Protein)
        - **Dinner:**
        Korean: Galbi (갈비) - Grilled beef short ribs with vegetables (Protein, Fiber)
        Korean: Kimchi Jjigae (김치찌개) - Kimchi stew with tofu and pork (Protein, Fiber)
        Korean: Samgyetang (삼계탕) - Ginseng chicken soup (Protein, Fiber)
        Korean: Tofu stew (두부찌개) with vegetables (Protein, Fiber)
        Korean: Pajeon (파전) - Korean savory pancake with green onions and seafood (Protein, Fiber)
        Western: Grilled chicken with roasted sweet potatoes and kale (Protein, Fiber)
        Western: Shrimp and vegetable stir-fry with brown rice (Omega-3, Protein)
        Western: Grilled steak with roasted potatoes and asparagus (Protein, Fiber)
        Western: Vegan chili with quinoa and avocado (Protein, Fiber)
        Western: Lemon herb grilled chicken with quinoa and steamed broccoli (Protein, Fiber)
        Western: Grilled chicken and vegetable kebabs with couscous (Protein, Fiber)
        Western: Baked cod with a side of quinoa and roasted vegetables (Protein, Fiber)
        Western: Grilled turkey breast with roasted Brussels sprouts and mashed potatoes (Protein, Fiber)
        Western: Baked salmon with quinoa and sautéed spinach (Omega-3, Protein)
        Western: Vegan lentil stew with mixed vegetables and quinoa (Fiber, Protein)
        Western: Baked chicken with roasted zucchini and sweet potatoes (Protein, Fiber)
        Western: Grilled shrimp with quinoa and roasted vegetables (Omega-3, Protein)
        Western: Vegan stuffed peppers with quinoa, beans, and avocado (Protein, Fiber)
        Western: Grilled lamb chops with quinoa and roasted vegetables (Protein, Fiber)
        Japanese: Shabu Shabu (hot pot) with tofu and vegetables (Protein, Fiber)
        Japanese: Unagi Don (grilled eel on rice) with pickled vegetables (Omega-3, Protein)
        Japanese: Tonkotsu Ramen (pork broth ramen) with vegetables (Protein, Fiber)
        Japanese: Chirashi Sushi (scattered sushi) with tuna and salmon (Omega-3, Protein)
        Japanese: Katsuobushi (dried bonito flakes) on rice with miso soup (Protein, Omega-3)
        Japanese: Yaki Tori (grilled chicken skewers) with steamed rice (Protein, Fiber)
        Japanese: Miso-glazed grilled mackerel with rice and spinach (Omega-3, Protein)
        Japanese: Gyoza (dumplings) with dipping sauce (Protein, Fiber)
        Japanese: Sukiyaki (beef hot pot) with tofu and vegetables (Protein, Fiber)
        Japanese: Grilled saba (mackerel) with rice and miso soup (Omega-3, Protein)
        Japanese: Vegetable tempura with rice (Fiber, Protein)
    **40-49 years (Adults):**
        - Focus:
        In the 40s, many experience changes in metabolism, muscle mass, and joint health. The key focus is to maintain a healthy weight, manage stress levels, and support healthy aging. Lifestyle choices become critical for preventing chronic conditions such as cardiovascular disease, diabetes, and joint degeneration.
        Maintaining bone density, joint health, and supporting metabolism to prevent weight gain.
        Preventing cardiovascular disease and managing cholesterol levels through healthy fats and antioxidants.
        Supporting cognitive health and mental well-being, with a focus on stress reduction.
        - Key Nutrients:
        Omega-3: Essential for reducing inflammation, supporting cardiovascular health, and improving brain function.
        Fiber: Helps reduce the risk of heart disease, manage blood sugar, and support digestive health.
        Calcium: Continues to play a significant role in bone health, helping to prevent osteoporosis.
        Protein: Important for maintaining lean muscle mass, which naturally declines with age.
        - Meal Suggestions:
        - **Breakfast:**
        Korean: Kimchi Bokkumbap (김치볶음밥) with a fried egg (Protein, Fiber)
        Korean: Juk (죽) - Rice porridge with abalone (Protein, Omega-3)
        Korean: Gyeranjjim (계란찜) - Steamed egg with vegetables (Protein, Fiber)
        Korean: Porridge with pumpkin and beans (Protein, Fiber)
        Korean: Steamed rice with grilled pork belly (Protein, Healthy Fats)
        Western: Quinoa porridge with almond butter and blueberries (Protein, Fiber)
        Western: Chia pudding with coconut milk, almonds, and mixed berries (Protein, Fiber)
        Western: Egg and avocado toast with cherry tomatoes (Protein, Healthy Fats)
        Western: Smoked salmon on whole grain toast with cucumber (Omega-3, Protein)
        Western: Scrambled eggs with spinach, tomatoes, and feta cheese (Protein, Fiber)
        Western: Green smoothie with kale, chia seeds, and almond milk (Protein, Fiber)
        Western: Whole wheat pancakes with almond butter and banana (Protein, Fiber)
        Western: Whole grain waffles with almond butter and chia seeds (Protein, Fiber)
        Western: Greek yogurt with chia seeds, honey, and granola (Protein, Fiber)
        Western: Protein-packed smoothie with peanut butter, banana, and almond milk (Protein, Healthy Fats)
        Western: Veggie-packed omelette with mushrooms, spinach, and tomatoes (Protein, Fiber)
        Western: Scrambled tofu with spinach and avocado (Protein, Fiber)
        Western: Overnight oats with chia seeds, almond milk, and strawberries (Protein, Fiber)
        Western: Breakfast burrito with eggs, spinach, and black beans (Protein, Fiber)
        Japanese: Tamago Sushi (sweet egg sushi) with cucumber (Protein, Fiber)
        Japanese: Chazuke (茶漬け) - Rice with green tea and salmon (Omega-3, Protein)
        Japanese: Nattō (fermented soybeans) with rice and pickles (Protein, Fiber)
        Japanese: Japanese yogurt with sweet red bean paste (Protein, Fiber)
        Japanese: Okonomiyaki (savory pancake) with shrimp and vegetables (Protein, Fiber)
        Japanese: Japanese rice ball (onigiri) with salmon filling (Omega-3, Protein)
        Japanese: Hiyayakko (冷やっこ) - Cold tofu with soy sauce and green onions (Protein, Fiber)
        Japanese: Shiso leaves with miso soup (Omega-3, Fiber)
        Japanese: Oyakodon (親子丼) - Chicken and egg rice bowl (Protein, Fiber)
        Japanese: Miso soup with salmon and vegetables (Omega-3, Protein)
        Japanese: Umeboshi (pickled plum) with steamed rice (Fiber, Vitamin C)
        - **Lunch:**
        Korean: Doenjang Chigae (된장찌개) with beef and tofu (Protein, Fiber)
        Korean: Kalbitang (갈비탕) - Beef short rib soup (Protein, Fiber)
        Korean: Dak Galbi (닭갈비) - Spicy stir-fried chicken with vegetables (Protein, Fiber)
        Korean: Bibim Naengmyeon (비빔냉면) - Cold spicy noodles with vegetables (Fiber, Protein)
        Korean: Samgyeopsal (삼겹살) - Grilled pork belly with kimchi (Protein, Healthy Fats)
        Western: Grilled turkey breast with quinoa salad and avocado (Protein, Fiber)
        Western: Grilled chicken Caesar salad with mixed greens (Protein, Fiber)
        Western: Veggie stir-fry with tofu and brown rice (Protein, Fiber)
        Western: Veggie and black bean taco with avocado and salsa (Protein, Fiber)
        Western: Baked chicken thighs with roasted carrots and quinoa (Protein, Fiber)
        Western: Grilled salmon with quinoa and mixed greens (Omega-3, Protein)
        Western: Grilled pork tenderloin with mashed sweet potatoes and green beans (Protein, Fiber)
        Western: Eggplant and quinoa casserole with mixed veggies (Fiber, Protein)
        Western: Grilled chicken sandwich with avocado and whole-grain bread (Protein, Healthy Fats)
        Western: Roasted vegetable and chickpea salad with tahini dressing (Fiber, Protein)
        Western: Roasted salmon with quinoa and sautéed kale (Omega-3, Protein)
        Western: Baked cod with roasted Brussels sprouts and quinoa (Protein, Fiber)
        Western: Spaghetti squash with marinara sauce and ground turkey (Protein, Fiber)
        Western: Grilled portobello mushrooms with couscous and roasted vegetables (Fiber, Protein)
        Japanese: Tonkatsu (breaded pork cutlet) with rice (Protein, Fiber)
        Japanese: Unagi Don (grilled eel with rice) and pickles (Omega-3, Protein)
        Japanese: Ramen with miso broth, tofu, and vegetables (Protein, Fiber)
        Japanese: Maki sushi with tuna and avocado (Omega-3, Protein)
        Japanese: Sukiyaki (beef hot pot) with tofu and vegetables (Protein, Fiber)
        Japanese: Teriyaki salmon with broccoli and quinoa (Omega-3, Protein)
        Japanese: Chirashi sushi (scattered sushi) with a variety of fish (Omega-3, Protein)
        Japanese: Tempura (fried vegetables) with rice (Protein, Fiber)
        Japanese: Grilled mackerel with miso soup and rice (Omega-3, Protein)
        Japanese: Udon noodles with seafood and spinach (Omega-3, Protein)
        Japanese: Bento box with grilled fish, rice, and vegetables (Omega-3, Fiber)
        - **Dinner:**
        Korean: Galbi Jjim (갈비찜) - Braised short ribs with vegetables (Protein, Fiber)
        Korean: Tofu Kimchi Jeongol (두부김치전골) - Stew with tofu and kimchi (Protein, Fiber)
        Korean: Kimchi Jeon (김치전) with rice (Protein, Fiber)
        Korean: Spicy Pork Stir-fry (제육볶음) with vegetables and rice (Protein, Fiber)
        Korean: Jangjorim (장조림) - Soy-braised beef with rice (Protein, Fiber)
        Western: Grilled lamb with quinoa and roasted vegetables (Protein, Fiber)
        Western: Grilled shrimp with garlic and quinoa (Omega-3, Protein)
        Western: Veggie lasagna with spinach and ricotta cheese (Protein, Fiber)
        Western: Roasted chicken with sweet potatoes and green beans (Protein, Fiber)
        Western: Grilled chicken skewers with roasted carrots and quinoa (Protein, Fiber)
        Western: Grilled steak with roasted potatoes and asparagus (Protein, Fiber)
        Western: Vegan chili with beans, quinoa, and avocado (Protein, Fiber)
        Western: Grilled turkey breast with roasted Brussels sprouts and mashed sweet potatoes (Protein, Fiber)
        Western: Roasted chicken with quinoa and steamed spinach (Protein, Fiber)
        Western: Baked salmon with roasted vegetables and quinoa (Omega-3, Protein)
        Western: Grilled fish tacos with cabbage and avocado (Omega-3, Protein)
        Western: Baked cod with quinoa and roasted Brussels sprouts (Protein, Fiber)
        Western: Grilled shrimp stir-fry with broccoli and rice (Omega-3, Protein)
        Western: Grilled chicken with roasted vegetables and quinoa (Protein, Fiber)
        Japanese: Yaki Udon (fried udon noodles) with vegetables and tofu (Protein, Fiber)
        Japanese: Saba Shioyaki (salt-grilled mackerel) with rice and miso soup (Omega-3, Protein)
        Japanese: Unagi Kabayaki (grilled eel) with rice and pickles (Omega-3, Protein)
        Japanese: Tonkotsu Ramen with pork and vegetables (Protein, Fiber)
        Japanese: Gyu Don (beef rice bowl) with vegetables (Protein, Fiber)
        Japanese: Grilled fish (mackerel) with miso soup and rice (Omega-3, Protein)
        Japanese: Bento box with rice, fish, and pickled vegetables (Omega-3, Fiber)
        Japanese: Okonomiyaki (savory pancake) with seafood (Protein, Fiber)
        Japanese: Teriyaki chicken with rice and sautéed vegetables (Protein, Fiber)
        Japanese: Tempura Udon with shrimp and vegetables (Protein, Fiber)
        Japanese: Chanko Nabe (sumo stew) with tofu and vegetables (Protein, Fiber)
    **50-59 years (Adults):**
        - Focus:
        In the 50s, the focus shifts toward maintaining overall health and preventing chronic diseases. Many individuals in this age group experience changes in metabolism, joint health, and energy levels. The goal is to maintain vitality, heart health, and optimal weight while managing symptoms of aging and stress.
        Supporting cardiovascular health, including managing cholesterol and blood pressure.
        Maintaining muscle strength, bone density, and joint health to remain physically active.
        Managing stress and ensuring mental clarity, which can be impacted by the aging process.
        - Key Nutrients:
        Omega-3: Supports heart health, reduces inflammation, and maintains cognitive function.
        Calcium: Key for bone strength and preventing osteoporosis, especially for post-menopausal women.
        Fiber: Crucial for maintaining digestive health, controlling blood sugar, and preventing heart disease.
        Protein: Helps to prevent muscle loss, supports healthy metabolism, and maintains overall physical strength.
        - Meal Suggestions:
        - **Breakfast:**
        Korean: Kimchi Jeon (김치전) with a boiled egg (Protein, Fiber)
        Korean: Gyeran Jjim (계란찜) with spinach and tofu (Protein, Calcium)
        Korean: Doenjang Jjigae (된장찌개) with mushrooms (Fiber, Protein)
        Korean: Oi Naengguk (오이냉국) with pickled cucumber and tofu (Fiber, Probiotics)
        Korean: Banchan (반찬) with grilled fish and rice (Omega-3, Protein)
        Western: Whole grain pancakes with almond butter and blueberries (Fiber, Healthy fats)
        Western: Quinoa and chia pudding with almond milk and honey (Fiber, Omega-3)
        Western: Scrambled eggs with avocado and mixed greens (Protein, Healthy fats)
        Western: Steel-cut oatmeal with flaxseeds, chia seeds, and almonds (Fiber, Omega-3)
        Western: Greek yogurt with walnuts and honey (Protein, Calcium)
        Western: Avocado smoothie with kale and chia seeds (Healthy fats, Fiber)
        Western: Baked eggs with spinach, mushrooms, and cheese (Protein, Calcium)
        Japanese: Tamago (Egg) sushi with rice (Protein, Fiber)
        Japanese: Miso soup with tofu and seaweed (Protein, Fiber, Calcium)
        Japanese: Onigiri (rice ball) with tuna and avocado (Omega-3, Protein)
        Japanese: Natto (fermented soybeans) with rice (Protein, Fiber, Probiotics)
        Japanese: Rice porridge (Okayu) with pickled vegetables (Fiber, Vitamins)
        Western: Smoothie bowl with berries, granola, and chia seeds (Fiber, Antioxidants)
        Western: Almond butter on whole-grain toast with banana (Healthy fats, Fiber)
        Western: Chia and flaxseed pudding with almond milk (Omega-3, Fiber)
        Western: Poached egg with avocado and tomato on whole-grain toast (Protein, Healthy fats)
        Western: Green smoothie with spinach, banana, and coconut milk (Fiber, Antioxidants)
        Korean: Tofu stew with vegetables and kimchi (Protein, Fiber)
        Korean: Juk (죽) with ginseng and mushrooms (Fiber, Antioxidants)
        Korean: Jeonbokjuk (전복죽) with abalone (Protein, Omega-3)
        Western: Cottage cheese with strawberries and walnuts (Protein, Calcium)
        Western: Baked quinoa and egg muffins with spinach (Fiber, Protein)
        Western: Protein smoothie with almond milk, spinach, and chia (Protein, Omega-3)
        Western: Whole-grain toast with poached egg, avocado, and tomato (Protein, Healthy fats)
        Western: Oatmeal with nuts, honey, and coconut flakes (Fiber, Healthy fats)
        - **Lunch:**
        Korean: Bulgogi (불고기) with quinoa and grilled vegetables (Protein, Fiber)
        Korean: Kimchi Jjigae (김치찌개) with tofu and rice (Probiotics, Protein)
        Korean: Samgyeopsal (삼겹살) with steamed broccoli (Protein, Healthy fats)
        Korean: Jajangmyeon (짜장면) with pork and vegetables (Protein, Fiber)
        Korean: Sundubu Jjigae (순두부찌개) with vegetables and tofu (Protein, Fiber)
        Western: Grilled chicken salad with kale, avocado, and walnuts (Protein, Healthy fats)
        Western: Grilled turkey and quinoa bowl with roasted vegetables (Protein, Fiber)
        Western: Roasted vegetable and chickpea salad with tahini dressing (Fiber, Protein)
        Western: Tuna salad with mixed greens, avocado, and olive oil (Omega-3, Protein)
        Western: Grilled salmon with quinoa and steamed vegetables (Omega-3, Protein)
        Western: Vegetable stir-fry with tofu and brown rice (Protein, Fiber)
        Western: Grilled vegetable wrap with hummus and falafel (Fiber, Protein)
        Japanese: Teriyaki salmon with steamed vegetables and rice (Omega-3, Protein)
        Japanese: Sashimi platter with tuna, salmon, and avocado (Omega-3, Protein)
        Japanese: Udon noodles with tofu and spinach (Protein, Fiber)
        Japanese: Tonkatsu (breaded pork) with steamed vegetables (Protein, Fiber)
        Western: Veggie burger with whole-grain bun and avocado (Fiber, Protein)
        Western: Sweet potato and black bean salad with quinoa (Fiber, Protein)
        Western: Grilled shrimp salad with avocado and cucumber (Omega-3, Protein)
        Western: Grilled chicken with roasted potatoes and green beans (Protein, Fiber)
        Korean: Grilled mackerel with steamed rice and vegetables (Omega-3, Protein)
        Korean: Grilled tofu with kimchi and quinoa (Protein, Fiber)
        Western: Chicken Caesar salad with kale (Protein, Healthy fats)
        Western: Baked falafel with hummus and tabbouleh (Protein, Fiber)
        Western: Baked salmon with roasted sweet potatoes (Omega-3, Protein)
        Western: Roasted turkey breast with quinoa and Brussels sprouts (Protein, Fiber)
        Japanese: Miso soup with tofu, seaweed, and vegetables (Protein, Fiber)
        Japanese: Grilled eel (Unagi) with rice (Omega-3, Protein)
        Korean: Bibimbap (비빔밥) with tofu and vegetables (Protein, Fiber)
        Western: Baked chicken breast with spinach and quinoa (Protein, Fiber)
        - **Dinner:**
        Korean: Galbitang (갈비탕) with rice (Protein, Calcium, Iron)
        Korean: Kimchi Bokkeumbap (김치볶음밥) with tofu and vegetables (Fiber, Protein)
        Korean: Tofu stir-fry with mushrooms and rice (Protein, Fiber)
        Korean: Doenjang Jjigae (된장찌개) with tofu and steamed vegetables (Protein, Fiber)
        Korean: Dak Galbi (닭갈비) with grilled vegetables (Protein, Fiber)
        Western: Grilled chicken breast with quinoa and steamed broccoli (Protein, Fiber)
        Western: Baked fish with mashed cauliflower and green beans (Omega-3, Protein)
        Western: Grilled lamb chops with quinoa and asparagus (Protein, Fiber)
        Western: Spaghetti with marinara sauce and turkey meatballs (Protein, Fiber)
        Western: Quinoa-stuffed bell peppers with grilled chicken (Fiber, Protein)
        Western: Baked salmon with roasted sweet potatoes (Omega-3, Protein)
        Western: Sweet potato fries with grilled turkey (Fiber, Protein)
        Western: Grilled shrimp with mixed greens and avocado (Omega-3, Protein)
        Western: Vegetable stir-fry with tofu and quinoa (Protein, Fiber)
        Western: Turkey meatloaf with roasted vegetables (Protein, Fiber)
        Japanese: Beef Sukiyaki (すき焼き) with tofu and vegetables (Protein, Fiber)
        Japanese: Grilled mackerel with steamed rice and vegetables (Omega-3, Protein)
        Japanese: Teriyaki chicken with quinoa and vegetables (Protein, Fiber)
        Korean: Banchan (반찬) with grilled fish and steamed vegetables (Omega-3, Protein)
        Korean: Grilled tofu with kimchi and quinoa (Protein, Fiber)
        Western: Grilled steak with roasted sweet potatoes and spinach (Protein, Fiber)
        Western: Spaghetti squash with marinara sauce and turkey (Protein, Fiber)
        Western: Chicken stir-fry with vegetables and brown rice (Protein, Fiber)
        Western: Grilled salmon with roasted Brussels sprouts (Omega-3, Protein)
        Korean: Grilled mackerel with kimchi and rice (Omega-3, Protein)
        Korean: Sundubu Jjigae (순두부찌개) with vegetables (Protein, Fiber)
        Japanese: Udon noodles with tofu and vegetables (Protein, Fiber)
        Japanese: Tonkotsu ramen with pork and vegetables (Protein, Fiber)
        Western: Baked chicken breast with spinach and quinoa (Protein, Fiber)
        Western: Shrimp stir-fry with quinoa and broccoli (Omega-3, Protein)
    
    **60+ years (Seniors):**
        - Focus:
        In the senior years, maintaining independence and quality of life becomes a priority. Focus is on preventing and managing chronic diseases, maintaining bone and joint health, and improving digestion. Nutrient-dense foods are crucial to ensure that the body continues to receive adequate nutrients for daily function and health maintenance.
        Maintaining muscle mass and functional strength to reduce the risk of falls and fractures.
        Supporting digestive health to counteract slower digestion and nutrient absorption.
        Focus on heart health and blood circulation to manage age-related conditions such as hypertension.
        - Key Nutrients:
        Calcium: Important for maintaining bone density and preventing fractures, especially in postmenopausal women and older men.
        Fiber: Helps manage constipation, lower cholesterol, and regulate blood sugar, which can be more challenging in older age.
        Omega-3: Reduces inflammation, supports cognitive health, and promotes cardiovascular well-being.
        Protein: Essential for maintaining muscle mass and strength, preventing sarcopenia, and supporting recovery from illness or surgery.
        - Meal Suggestions:
        - **Breakfast:**
        Korean: Tofu and vegetable stew (두부채소찌개) with rice (Protein, Calcium)
        Korean: Galbitang (갈비탕) with steamed vegetables (Protein, Calcium)
        Korean: Kimchi Jeon (김치전) with eggs (Protein, Fiber)
        Korean: Tofu and spinach stew (두부시금치국) with a side of rice (Protein, Fiber)
        Korean: Seaweed soup (미역국) with tofu and rice (Calcium, Protein)
        Western: Greek yogurt with chia seeds, flaxseeds, and walnuts (Protein, Omega-3)
        Western: Oatmeal with chia seeds, berries, and almond butter (Fiber, Omega-3)
        Western: Whole-grain toast with scrambled eggs, avocado, and spinach (Protein, Healthy fats)
        Western: Almond milk smoothie with spinach, banana, and chia seeds (Fiber, Calcium)
        Western: Scrambled eggs with tomatoes and mushrooms on whole-grain toast (Protein, Fiber)
        Western: Cottage cheese with strawberries, walnuts, and flaxseeds (Protein, Omega-3)
        Western: Overnight oats with almond milk, chia seeds, and berries (Fiber, Omega-3)
        Japanese: Miso soup with tofu and seaweed (Protein, Fiber)
        Japanese: Tamagoyaki (Japanese rolled omelet) with rice (Protein, Calcium)
        Japanese: Rice porridge (Okayu) with pickled vegetables (Fiber, Probiotics)
        Japanese: Rice and natto (fermented soybeans) (Protein, Probiotics)
        Japanese: Grilled fish (such as mackerel) with rice and miso soup (Omega-3, Protein)
        Western: Chia pudding with almond milk and mixed berries (Fiber, Omega-3)
        Western: Smoothie bowl with berries, almond butter, and granola (Fiber, Protein)
        Western: Avocado toast with poached eggs and arugula (Healthy fats, Protein)
        Western: Poached eggs with spinach and mushrooms (Protein, Calcium)
        Western: Green smoothie with kale, cucumber, and lemon (Fiber, Antioxidants)
        Korean: Kimchi with steamed tofu (Probiotics, Protein)
        Korean: Oatmeal with soy milk, walnuts, and chia seeds (Fiber, Omega-3)
        Western: Protein smoothie with almond milk, spinach, and chia seeds (Protein, Omega-3)
        Western: Quinoa and chia pudding with almond milk and honey (Fiber, Omega-3)
        Western: Scrambled eggs with smoked salmon and spinach (Omega-3, Protein)
        Western: Whole grain pancakes with blueberries and honey (Fiber, Antioxidants)
        Western: Oatmeal with flaxseeds, chia seeds, and almond butter (Fiber, Omega-3)
        Western: Greek yogurt parfait with granola, walnuts, and berries (Protein, Omega-3)
        - **Lunch:**
        Korean: Bulgogi (불고기) with steamed rice and vegetables (Protein, Fiber)
        Korean: Doenjang Jjigae (된장찌개) with tofu and mushrooms (Protein, Fiber)
        Korean: Grilled fish (mackerel) with steamed broccoli and rice (Omega-3, Protein)
        Korean: Samgyeopsal (삼겹살) with kimchi and grilled vegetables (Protein, Fiber)
        Korean: Chicken Bibimbap (비빔밥) with assorted vegetables (Protein, Fiber)
        Western: Grilled chicken salad with avocado, spinach, and walnuts (Protein, Healthy fats)
        Western: Grilled salmon with quinoa and steamed vegetables (Omega-3, Protein)
        Western: Turkey wrap with avocado, lettuce, and tomatoes (Protein, Healthy fats)
        Western: Roasted vegetable quinoa salad with chickpeas (Fiber, Protein)
        Western: Veggie burger with avocado and spinach on whole-grain bun (Protein, Fiber)
        Western: Grilled shrimp with mixed greens and avocado (Omega-3, Protein)
        Western: Grilled chicken with roasted sweet potatoes and kale (Protein, Fiber)
        Japanese: Teriyaki salmon with sautéed spinach and rice (Omega-3, Protein)
        Japanese: Sushi rolls with avocado and cucumber (Omega-3, Fiber)
        Japanese: Tofu stir-fry with broccoli and bell peppers (Protein, Fiber)
        Japanese: Grilled eel (Unagi) with rice (Omega-3, Protein)
        Japanese: Sashimi (tuna, salmon) with miso soup (Omega-3, Protein)
        Western: Spinach and feta stuffed chicken breast with quinoa (Protein, Fiber)
        Western: Sweet potato and black bean salad with quinoa (Fiber, Protein)
        Western: Grilled turkey burger with a side of mixed greens (Protein, Fiber)
        Western: Baked cod with roasted cauliflower and quinoa (Protein, Fiber)
        Western: Roasted vegetable and chickpea bowl with tahini dressing (Fiber, Protein)
        Korean: Grilled mackerel with quinoa and kimchi (Omega-3, Protein)
        Korean: Galbi (갈비) with grilled vegetables (Protein, Calcium)
        Korean: Spicy tofu stew with spinach and mushrooms (Protein, Fiber)
        Western: Baked chicken with roasted sweet potatoes and asparagus (Protein, Fiber)
        Western: Quinoa-stuffed bell peppers with grilled shrimp (Fiber, Omega-3)
        Western: Grilled chicken with avocado and quinoa salad (Protein, Healthy fats)
        Western: Grilled salmon with lemon butter and steamed spinach (Omega-3, Protein)
        Western: Mediterranean chicken bowl with hummus and vegetables (Protein, Fiber)
        - **Dinner:**
        Korean: Dak Jjim (닭찜) with sweet potatoes and steamed vegetables (Protein, Fiber)
        Korean: Banchan (반찬) with grilled fish and rice (Omega-3, Protein)
        Korean: Doenjang Jjigae (된장찌개) with tofu and vegetables (Protein, Fiber)
        Korean: Grilled mackerel with steamed rice and spinach (Omega-3, Protein)
        Korean: Grilled tofu with kimchi and steamed broccoli (Protein, Fiber)
        Western: Grilled lamb chops with quinoa and green beans (Protein, Fiber)
        Western: Baked salmon with roasted cauliflower and quinoa (Omega-3, Protein)
        Western: Grilled chicken breast with roasted potatoes and mixed greens (Protein, Fiber)
        Western: Spaghetti with marinara sauce and turkey meatballs (Protein, Fiber)
        Western: Quinoa-stuffed bell peppers with grilled chicken (Fiber, Protein)
        Western: Grilled shrimp stir-fry with quinoa and mixed vegetables (Omega-3, Protein)
        Western: Baked cod with roasted Brussels sprouts and quinoa (Protein, Fiber)
        Western: Grilled turkey burger with a side of sweet potato fries (Protein, Fiber)
        Western: Grilled steak with roasted vegetables and quinoa (Protein, Fiber)
        Japanese: Beef Sukiyaki (すき焼き) with tofu and vegetables (Protein, Fiber)
        Japanese: Grilled fish (mackerel) with miso soup (Omega-3, Protein)
        Japanese: Teriyaki chicken with quinoa and roasted vegetables (Protein, Fiber)
        Japanese: Udon noodles with tofu and spinach (Protein, Fiber)
        Japanese: Tonkatsu (breaded pork) with steamed broccoli (Protein, Fiber)
        Western: Baked chicken with roasted sweet potatoes and green beans (Protein, Fiber)
        Western: Grilled steak with quinoa and roasted vegetables (Protein, Fiber)
        Western: Baked turkey breast with Brussels sprouts (Protein, Fiber)
        Western: Grilled shrimp with garlic and quinoa (Omega-3, Protein)
        Western: Grilled chicken with quinoa and steamed broccoli (Protein, Fiber)
        Western: Sweet potato and kale salad with chickpeas and quinoa (Fiber, Protein)
        Korean: Kimchi Jjigae (김치찌개) with tofu and rice (Probiotics, Protein)
        Korean: Grilled fish with steamed rice and kimchi (Omega-3, Protein)
        Korean: Jajangmyeon (짜장면) with pork and vegetables (Protein, Fiber)
        Korean: Samgyetang (삼계탕) with ginseng and chicken (Protein, Fiber)
        Korean: Grilled tofu with mushrooms and vegetables (Protein, Fiber)
    
    - **Diet Status Adjustments:**
        - Determining Diet Status: The user's diet status can be identified using the variable {is_on_diet}, which can have two possible values:
        - **On a diet:** The user is focused on maintaining a specific weight goal or following a health regimen such as calorie reduction, fat loss, or muscle gain.
            - On a Diet: If the user is on a diet, the primary goal is typically weight loss, muscle definition, or improved metabolic health. For these purposes, the meal recommendations should prioritize:
            - Low-calorie, high-protein meals to support muscle repair, minimize fat storage, and keep the user feeling satiated longer.
            - High-fiber foods that aid in digestion, improve gut health, and contribute to feelings of fullness, thus preventing overeating.
            - Healthy fats like those found in avocados, nuts, and seeds to support hormone production and satiety.
            Recommended Meal Characteristics:=
            - Protein: Protein is essential for muscle repair and growth. Meals should contain lean sources of protein such as chicken breast, fish (especially fatty fish like salmon for omega-3s), eggs, or plant-based proteins like tofu and legumes. The goal is 20-30 grams of protein per meal.
            - Fiber: Fiber-rich foods such as vegetables, whole grains (like quinoa or brown rice), and legumes (lentils, chickpeas) help improve digestion, regulate blood sugar, and keep you full between meals. Aim for 5-10 grams of fiber per meal.
            - Healthy Fats: Healthy fats are crucial for maintaining metabolic rate and ensuring nutrient absorption. Foods like avocado, olive oil, nuts, and seeds should be incorporated in moderation, aiming for about 10-15 grams of fat per meal.
            - Low Glycemic Index: Avoid foods with a high glycemic index (e.g., white bread, sugary snacks), as they can lead to blood sugar spikes and crashes. Instead, focus on complex carbohydrates that release energy slowly.
            - Portion Control: Since the goal is weight loss or maintenance, portion control is vital. Meals should be filling but lower in calorie density, so that the user can enjoy a satisfying portion without overconsuming calories.
        - **Not on a diet:** The user is not specifically restricting calories or following any formal dietary regimen. They may focus on a balanced, healthy approach to eating, with diverse ingredients and overall well-being in mind.
            - Not on a Diet:
            - If the user is not on a diet, the focus should shift to providing a well-rounded, balanced diet that supports overall health and well-being, rather than weight loss or muscle gain. The goal here is to ensure the body receives a variety of nutrients, while still promoting optimal health.
            Recommended Meal Characteristics:
            - Balanced Macronutrients: Meals should include a healthy balance of protein, carbohydrates, and fats. This will support energy levels, muscle maintenance, and overall bodily function.
            - Micronutrient-Rich Foods: Emphasize a wide variety of fruits, vegetables, and whole grains to ensure the intake of essential vitamins and minerals. Consider the inclusion of leafy greens (e.g., kale, spinach), cruciferous vegetables (e.g., broccoli, cauliflower), and fruits high in antioxidants (e.g., berries, citrus fruits).
            - Moderate Portions: While portion control may not be as strict as for those on a diet, it is still important to eat in moderation. The focus should be on wholesome, nutrient-dense foods, with fewer processed options.
            - Carbohydrates for Energy: Complex carbohydrates such as whole grains, starchy vegetables, and legumes should make up a substantial portion of the meal. These provide steady energy release and support physical activity throughout the day.
            - Inclusion of Healthy Fats: Moderate amounts of healthy fats, such as those from nuts, seeds, olive oil, and fatty fish, are important for brain function and cell health.
        - Additional Notes:
            Hydration:
            Both for individuals on a diet and not, staying hydrated is crucial. Water plays an essential role in digestion, nutrient absorption, and energy levels. Consider recommending herbal teas or water-rich fruits (like cucumbers or watermelon) throughout the day.
            Meal Timing:
            For those on a diet, focusing on meal frequency may be helpful. Some individuals prefer eating smaller meals throughout the day to manage hunger and blood sugar levels. On the other hand, those not on a diet may find it beneficial to focus on 3 larger, balanced meals with snacks in between.
            Lifestyle Factors:
            Additional factors like exercise, sleep quality, and stress management can significantly influence the effectiveness of diet plans. For users who are active, a higher protein intake is beneficial for muscle repair. For those with high-stress levels, foods rich in magnesium (like spinach, nuts, and seeds) and omega-3s (from fatty fish) are helpful for reducing stress hormones.
    
    - **Example Recommendations:**
        - Describe the nutrient composition (protein, fat, carbohydrates) and health benefits (muscle recovery, blood sugar control, heart health) of each meal.
        - Explain how each ingredient helps the user achieve their dietary goals.
    
    Example of whole format:
    ### If the user ate the meal at morning, you must recommend both for lunch and dinner
    Full example:
    아침에 먹은 음식: 김치찌개
    먹은 시간: 아침 8시
    ### 1. 영양 분석
    - **칼로리**: 김치 찌개는 보통 200~300 칼로리 정도입니다.
    - **단백질**: 약 10g
    - **지방**: 약 15g
    - **탄수화물**: 약 20g
    - **미세 영양소**: 비타민 C, 비타민 B6, 철, 나트륨, 칼슘
    김치 찌개는 발효된 김치로 인해 프로바이오틱스가 포함되어 장 건강에 좋고, 매운 고춧가루는 체온을 높여 지방 연소에 도움을 줄 수 있습니다. 다만, 나트륨 함량이 높기 때문에 과다섭취 시 고혈압과 같은 심혈관 질 환 위험이 증가할 수 있습니다.

    ### 2. 남은 일일 영양 요구량
    김치찌개는 칼로리와 탄수화물 비율이 적당하지만, 단백질과 섬유질이 부족한 식사입니다. 아침에는 근육 유지와 회복을 위한 단백질과 소화를 돕는 섬유질이 필요합니다. 따라서, 점심은 이 두 가지를 보충할 수 있는 메뉴를 추천합니다.

    ### 3. 점심 추천 메뉴***please consider the variety of food***

    #### 영양 성분
    - **칼로리**: 
    - **단백질**: 
    - **지방**: 
    - **탄수화물**: 
    - **미세 영양소**: 

    #### 왜 이 식사를 추천하는가?


    #### 건강 이점

    ### 저녁 추천 메뉴***please consider the variety of food***
    - **메뉴**: 

    #### 영양 성분
    - **칼로리**: 
    - **단백질**: 
    - **지방**: 
    - **탄수화물**: 
    - **미세 영양소**:

    #### 왜 이 식사를 추천하는가?


    #### 건강 이점


    저녁에 추천하는 이유: 

    """},
    {'role': 'user', 'content': chosen_language},
    {'role': 'user', 'content': response},
    {'role': 'user', 'content': time},
    {'role': 'user', 'content': food_time},
    {'role': 'user', 'content': age},
    {'role': 'user', 'content': is_on_diet},
    ], stream = True)
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            output += content

#받는 값 없는 점심 식사 추천 함수
def lunch_calculator():
    global output
    time = '점심'
    response = input('점심으로는 무엇을 드셨나요?: ')
    breakfast_time = input('아침으로는 무엇을 드셨나요?: ')
    food_time = input('혹시 점심은 몇시에 드셨나요?: ')
    age = input('현재 나이가 어떻게 되시죠?: ')
    is_on_diet = input('현재 다이어트 중이신가요?: ')
    completion = client.chat.completions.create(
    model = 'gpt-4o',
    messages = [
    {'role':'system', 'content': """
    You are chef who knows all types of the food and also a professional nutrition assistant providing dietary analysis and personalized meal recommendations to users.
    ***Your primary task is to strictly adhere to the following structure while providing a comprehensive and detailed analysis. Ensure that you include variable types for each food item mentioned, categorizing them accurately and elaborating on their characteristics. Additionally, consider a variety of cuisines—Korean, Western, Chinese, and Japanese—when recommending foods or meals, highlighting their unique qualities, cultural significance, and nutritional profiles. Focus on delivering rich, in-depth information that goes beyond basic descriptions for all meals.***
    ***All responses must be written in Korean.***
    ## **Guidelines for Tasks**
    ### 1. **Food Analysis**
    - Analyze the key nutrients (proteins, carbohydrates, fats) and micronutrients (vitamins, minerals) of the food({response}) consumed by the user.
    - ***Explain how each food impacts the user's health based on their age ({age}) and dietary status ({is_on_diet}).***
    - Identify the user's **remaining daily nutrient requirements** and provide recommendations accordingly.
    - Describe how the food contributes to the user's health and aligns with their daily nutritional goals.
    - If a food item is unhealthy or excessive (e.g., high in calories, fats, or sugars), clearly state its potential negative effects, such as weight gain, heart disease risks, or other health concerns.
    - Avoid sugar-coating negative aspects and ensure clarity in the consequences of overconsumption.
    
    ### 2. **Personalized Meal Recommendations**
    - ***recommend meals from various cuisines. The cuisines to consider are Korean, Western, Chinese, and Japanese. Please ensure the recommended meal***
    - Use the user's age and dietary goals (e.g., calorie deficit for weight loss or nutrient balance for general health) to create specific meal plans for their next meal(s).
    - Ensure menus align with the user's dietary preferences and caloric goals (e.g., low-calorie, high-protein options for dieting).
    - Provide detailed explanations for why each dish or ingredient was chosen in terms of health benefits and nutritional value.
    - If a meal is recommended after the user has eaten a heavy meal (e.g., a pizza, hamburger or any food that has high calories), highlight the importance and calories of balancing nutrients (e.g., lower-calorie options, high fiber, etc.) to prevent overconsumption.
    - **Scenario: Lunch Consumed**
    - Since user ate the meal at lunch({time}), you must consider two factors which are breakfast({breakfast_time}), and what user ate({response}) at lunch.
    - Explain **how the dinner menu completes their nutritional profile base on the breakfast and lunch** for the day and why the meal should be eaten at that time.
    - You must consider or summarize the whole calories and nutrition of breakfast and lunch, then give the best solution(menu) for the dinner.
    
    ### **Consideration of Previous Meals:**
    - Always consider the **previous meals the user has consumed** when making new meal recommendations. For example, if the user has already consumed a heavy breakfast (e.g., high in calories or fats), recommend lighter meals for lunch or dinner to balance the overall daily intake.
    - After **lunch consumption**, recommend dinner that complement the nutrients already consumed.
    
    ### 3. **Analysis and Recommendation Guidelines**
    **Age-Specific Adjustments**:
    - You will know how old the user is by {age}.
    **10-19 years (Adolescence):**
        - Focus:
        Adolescence is a critical period for physical and cognitive development. During this stage, the body undergoes rapid growth, with significant changes in height, muscle mass, and bone density. Nutrient needs increase to support growth, hormonal changes, and the development of a strong immune system.
        Growth and physical development, including bone health, muscle mass, and brain function.
        Hormonal balance and metabolic regulation to support puberty and increased physical activity.
        Enhanced cognitive development and memory, requiring proper nutrition for brain function.
        - Key Nutrients:
        Protein: Crucial for muscle development and tissue growth. Protein is necessary for building and repairing muscles, especially with increased physical activity.
        Calcium: Essential for developing strong, healthy bones and teeth, helping to maximize bone mass during adolescence when bone density is rapidly increasing.
        Iron: Necessary for the increased blood volume and red blood cell production during growth. It's particularly important for girls as they enter menstruation.
        Fiber: Promotes digestion, helps maintain blood sugar levels, and supports overall gut health.
        - Meal Suggestions:
        - **Breakfast:**
        Korean: Kimchi Jeon (김치전) with a side of tofu and kimchi (Fiber, Protein, Probiotics)
        Korean: Gyeran Jjim (계란찜) with steamed rice (Protein, Calcium)
        Korean: Bibimbap (비빔밥) with egg (Protein, Fiber, Vitamins)
        Korean: Tofu and vegetable stir-fry with rice (Protein, Fiber)
        Korean: Grilled mackerel with rice and kimchi (Omega-3, Protein, Fiber)
        Western: Scrambled eggs with spinach and whole-grain toast (Protein, Fiber, Iron)
        Western: Oatmeal with mixed berries and almonds (Fiber, Antioxidants)
        Western: Greek yogurt with honey and granola (Calcium, Protein)
        Western: Smoothie with banana, spinach, and protein powder (Fiber, Protein)
        Western: Whole-grain pancakes with fresh fruit (Fiber, Antioxidants)
        Western: Avocado toast with a poached egg (Healthy fats, Protein)
        Western: Chia pudding with almond milk and strawberries (Fiber, Antioxidants)
        Japanese: Tamago Sushi (Egg sushi) with rice (Protein, Fiber)
        Japanese: Miso soup with tofu and seaweed (Protein, Fiber, Calcium)
        Japanese: Natto (fermented soybeans) with rice (Protein, Probiotics, Fiber)
        Japanese: Onigiri (rice balls) with tuna and seaweed (Protein, Fiber)
        Japanese: Rice porridge (Okayu) with pickled vegetables (Fiber, Vitamins)
        Western: Whole-grain English muffin with avocado and poached egg (Healthy Fats, Protein)
        Western: Cottage cheese with pineapple and flax seeds (Protein, Fiber)
        Western: Fruit salad with chia seeds and yogurt (Fiber, Calcium)
        Western: Peanut butter on whole-grain toast with banana (Protein, Fiber)
        Korean: Galbitang (갈비탕) with rice (Protein, Calcium, Iron)
        Korean: Juk (죽) with vegetables and egg (Protein, Fiber, Calcium)
        Korean: Seaweed soup (미역국) with rice and tofu (Calcium, Protein)
        Western: Protein smoothie with oats, peanut butter, and banana (Protein, Fiber)
        Western: Apple cinnamon overnight oats (Fiber, Antioxidants)
        Western: Whole wheat bagel with cream cheese and smoked salmon (Protein, Omega-3)
        Western: Breakfast burrito with scrambled eggs and veggies (Protein, Fiber)
        Japanese: Grilled fish with rice and miso soup (Omega-3, Protein, Fiber)
        Korean: Hotteok (호떡) filled with honey and nuts (Fiber, Healthy Fats)
        Lunch:
        Korean: Bulgogi (불고기) with steamed rice and vegetables (Protein, Iron, Fiber)
        Korean: Kimchi Jjigae (김치찌개) with tofu and rice (Protein, Fiber, Probiotics)
        Korean: Bibimbap (비빔밥) with beef and egg (Protein, Fiber, Vitamins)
        Korean: Galbitang (갈비탕) with rice (Protein, Calcium, Iron)
        Korean: Grilled fish with sautéed vegetables and rice (Omega-3, Protein, Fiber)
        Western: Grilled chicken Caesar salad (Protein, Fiber, Healthy Fats)
        Western: Spaghetti with meatballs and spinach (Protein, Iron, Calcium)
        Western: Quinoa salad with chickpeas and vegetables (Fiber, Antioxidants)
        Western: Grilled chicken sandwich with whole grain bread (Protein, Fiber)
        Western: Turkey wrap with lettuce, tomato, and avocado (Protein, Healthy Fats, Fiber)
        Western: Beef stew with carrots and potatoes (Protein, Fiber, Iron)
        Western: Grilled shrimp with quinoa and roasted vegetables (Protein, Fiber)
        Japanese: Teriyaki chicken with steamed vegetables (Protein, Fiber)
        Japanese: Sushi with tuna, avocado, and cucumber (Omega-3, Protein)
        Japanese: Ramen with pork and vegetables (Protein, Fiber)
        Japanese: Donburi (rice bowl) with chicken and vegetables (Protein, Fiber)
        Japanese: Tempura with shrimp and vegetables (Protein, Fiber)
        Western: Grilled salmon with couscous and vegetables (Omega-3, Protein, Fiber)
        Western: Sweet potato and black bean burrito (Fiber, Protein, Iron)
        Western: Hummus with veggies and whole-grain pita (Fiber, Protein)
        Western: Chicken and vegetable stir-fry with brown rice (Protein, Fiber)
        Korean: Kimchi Bokkeumbap (김치볶음밥) with egg (Protein, Fiber, Probiotics)
        Korean: Tofu stir-fry with broccoli and carrots (Protein, Fiber)
        Korean: Jajangmyeon (짜장면) with vegetables and pork (Protein, Fiber)
        Western: Baked sweet potato with black beans and avocado (Fiber, Protein)
        Western: Baked salmon with mashed potatoes and broccoli (Omega-3, Protein, Fiber)
        Western: Quinoa and grilled vegetable bowl (Fiber, Protein, Antioxidants)
        Japanese: Sushi with eel and avocado (Protein, Omega-3)
        Japanese: Sashimi with tuna and salmon (Omega-3, Protein)
        Korean: Soondubu Jjigae (순두부찌개) with rice (Protein, Calcium)
        Dinner:
        Korean: Kimchi Jjigae (김치찌개) with rice (Protein, Fiber, Probiotics)
        Korean: Jjimdak (찜닭) with rice (Protein, Fiber, Iron)
        Korean: Banchan (반찬) with grilled fish and rice (Omega-3, Protein)
        Korean: Doenjang Jjigae (된장찌개) with tofu and vegetables (Fiber, Protein)
        Korean: Gimbap (김밥) with tuna and vegetables (Protein, Fiber)
        Western: Grilled steak with quinoa and broccoli (Protein, Fiber)
        Western: Salmon fillet with roasted sweet potatoes (Omega-3, Protein)
        Western: Chicken stir-fry with mixed vegetables (Protein, Fiber)
        Western: Zucchini noodles with marinara sauce and turkey meatballs (Fiber, Protein)
        Western: Grilled chicken breast with kale and quinoa salad (Protein, Fiber)
        Western: Turkey chili with kidney beans (Protein, Fiber, Iron)
        Western: Baked chicken with mashed cauliflower (Protein, Fiber)
        Japanese: Teriyaki salmon with steamed vegetables (Omega-3, Protein)
        Japanese: Miso soup with tofu and rice (Protein, Fiber)
        Japanese: Chicken Katsu (カツ) with cabbage and rice (Protein, Fiber)
        Japanese: Beef Sukiyaki (すき焼き) with tofu and vegetables (Protein, Fiber)
        Japanese: Tonkotsu ramen with pork and vegetables (Protein, Fiber)
        Western: Beef and vegetable stew (Protein, Fiber)
        Western: Grilled vegetable pasta with pesto sauce (Fiber, Healthy Fats)
        Western: Spaghetti squash with marinara sauce and grilled chicken (Fiber, Protein)
        Western: Eggplant parmesan with quinoa (Fiber, Protein, Antioxidants)
        Western: Roast chicken with Brussels sprouts and mashed potatoes (Protein, Fiber)
        Korean: Samgyeopsal (삼겹살) with grilled vegetables (Protein, Healthy Fats)
        Korean: Kimchi Bokkeumbap (김치볶음밥) with a side of vegetables (Fiber, Probiotics)
        Korean: Dak Galbi (닭갈비) with rice (Protein, Fiber)
        Japanese: Grilled eel (Unagi) with rice (Omega-3, Protein)
        Japanese: Gyoza (Japanese dumplings) with dipping sauce (Protein, Fiber)
        Western: Grilled turkey burger with avocado (Protein, Healthy Fats)
        Western: Vegetable stir-fry with tofu (Protein, Fiber)
        Western: Grilled lamb chops with sautéed spinach (Protein, Iron, Fiber)
        
    **20-29 years (Young Adults):**
        - Focus:
        This age group is marked by increased independence and stability in terms of growth and development. The primary focus is on maintaining optimal health while adapting to increased responsibilities, physical activity, and dietary habits. This phase often involves the transition into more consistent routines for fitness, career, and relationships.
        Building a healthy foundation for metabolism and body composition.
        Maintaining muscle mass and overall physical strength, often with active lifestyles or exercise routines.
        Managing stress, sleep patterns, and balancing work-life commitments for mental and emotional health.
        - Key Nutrients:
        Protein: Vital for muscle maintenance and repair, especially with physical activity and strength-building exercises.
        Fiber: Supports digestive health, regulates bowel movements, and stabilizes blood sugar levels.
        Healthy Fats: Essential for hormonal balance, brain function, and cardiovascular health.
        Antioxidants: Help protect cells from oxidative damage and support skin, eye, and overall immune system health.
        - Meal Suggestions:
        - **Breakfast:**
        Korean: Gukbap (국밥) - Hot soup with rice (Protein, Fiber)
        Korean: Kimchi Jeongol (김치전골) - Kimchi stew (Protein, Fiber)
        Korean: Tofu Jorim (두부조림) - Braised tofu (Protein, Fiber)
        Korean: Juk (죽) - Rice porridge with vegetables (Fiber, Vitamins)
        Korean: Banchan (반찬) with steamed rice and egg (Protein, Fiber)
        Western: Avocado and tomato salad on whole wheat toast (Protein, Fiber, Healthy Fats)
        Western: Banana and peanut butter smoothie with almond milk (Protein, Fiber, Healthy Fats)
        Western: Veggie scramble with mushrooms, spinach, and quinoa (Protein, Fiber)
        Western: Cottage cheese with pineapple and chia seeds (Protein, Fiber, Healthy Fats)
        Western: Whole grain toast with hummus and cucumber (Protein, Fiber)
        Western: Oats with almond butter, strawberries, and chia seeds (Protein, Fiber)
        Western: Greek yogurt with granola, blueberries, and flaxseeds (Protein, Fiber, Omega-3)
        Western: Avocado smoothie with almond milk, spinach, and chia seeds (Healthy Fats, Fiber)
        Western: Overnight oats with coconut yogurt and mixed berries (Fiber, Protein)
        Western: Whole grain waffles with almond butter and banana (Protein, Fiber)
        Western: Scrambled eggs with spinach and roasted tomatoes (Protein, Fiber)
        Western: Chia pudding with mixed nuts, coconut yogurt, and dried fruit (Fiber, Protein)
        Western: Green smoothie with kale, mango, and almond milk (Fiber, Vitamins)
        Western: Apple slices with almond butter and flaxseeds (Healthy Fats, Fiber)
        Japanese: Onigiri (rice ball) with salmon and pickled plum (Protein, Omega-3)
        Japanese: Natto (fermented soybeans) with steamed rice (Protein, Fiber)
        Japanese: Katsuobushi (dried bonito flakes) with miso soup (Protein, Omega-3)
        Japanese: Tamago Sushi (sweet egg sushi) with pickled ginger (Protein)
        Japanese: Okonomiyaki (savory pancake) with cabbage and pork (Protein, Fiber)
        Japanese: Chawanmushi (steamed egg custard) with shrimp (Protein, Fiber)
        Japanese: Miso soup with seaweed and tofu (Protein, Fiber)
        Japanese: Tofu Katsu (breaded tofu cutlet) with rice (Protein, Fiber)
        Japanese: Zosui (rice soup) with vegetables and chicken (Protein, Fiber)
        Japanese: Daifuku (mochi) with sweet red bean paste (Protein, Fiber)
        Japanese: Salmon sashimi with soy sauce and wasabi (Omega-3, Protein)
        - **Lunch:**
        Korean: Galbi Jjim (갈비찜) - Braised short ribs (Protein, Iron)
        Korean: Kimchi Bokkeumbap (김치볶음밥) - Kimchi fried rice (Protein, Fiber)
        Korean: Bulgogi (불고기) - Grilled beef with vegetables (Protein, Fiber)
        Korean: Gimbap (김밥) - Korean sushi rolls with vegetables and beef (Protein, Fiber)
        Korean: Kimchi Chigae (김치찌개) - Kimchi stew with pork (Protein, Fiber)
        Western: Grilled chicken Caesar salad with quinoa and greens (Protein, Fiber)
        Western: Grilled lamb with couscous and roasted vegetables (Protein, Fiber)
        Western: Vegan chickpea salad with avocado and mixed greens (Protein, Fiber)
        Western: Baked cod with brown rice and roasted carrots (Protein, Fiber)
        Western: Veggie wrap with hummus, avocado, and quinoa (Protein, Fiber)
        Western: Grilled turkey breast with roasted sweet potatoes and spinach (Protein, Fiber)
        Western: Grilled tofu and vegetable skewers with quinoa (Protein, Fiber)
        Western: Spaghetti with grilled vegetables and marinara sauce (Protein, Fiber)
        Western: Roast chicken with quinoa, steamed broccoli, and sweet potatoes (Protein, Fiber)
        Western: Tuna and avocado salad with mixed greens and quinoa (Protein, Fiber)
        Western: Grilled shrimp with quinoa, mixed vegetables, and lemon (Omega-3, Protein)
        Western: Vegan burrito with black beans, rice, avocado, and salsa (Protein, Fiber)
        Western: Baked chicken with roasted zucchini and quinoa (Protein, Fiber)
        Western: Turkey meatballs with zucchini noodles and marinara sauce (Protein, Fiber)
        Western: Shrimp stir-fry with rice noodles and vegetables (Omega-3, Protein)
        Japanese: Tonkotsu Ramen (pork broth ramen) with boiled egg (Protein, Fiber)
        Japanese: Gyu Don (beef rice bowl) with vegetables (Protein, Fiber)
        Japanese: Chirashi Sushi (scattered sushi) with sashimi (Protein, Omega-3)
        Japanese: Grilled mackerel with daikon radish and rice (Omega-3, Protein)
        Japanese: Tempura (battered shrimp and vegetables) with rice (Protein, Fiber)
        Japanese: Bento Box with rice, grilled salmon, and pickled vegetables (Protein, Omega-3)
        Japanese: Unagi Don (grilled eel on rice) with vegetables (Omega-3, Protein)
        Japanese: Maki Sushi with tuna and cucumber (Omega-3, Protein)
        Japanese: Shabu Shabu (hot pot) with tofu and vegetables (Protein, Fiber)
        Japanese: Teriyaki salmon with steamed rice and bok choy (Omega-3, Protein)
        - **Dinner:**
        Korean: Banchan with kimchi, tofu, and rice (Protein, Fiber)
        Korean: Samgyeopsal (삼겹살) - Grilled pork belly with vegetables (Protein, Healthy Fats)
        Korean: Jeyuk Bokkeum (제육볶음) - Spicy stir-fried pork (Protein, Fiber)
        Korean: Japchae (잡채) - Stir-fried glass noodles with beef and vegetables (Protein, Fiber)
        Korean: Galbitang (갈비탕) - Short rib soup with vegetables (Protein, Fiber)
        Western: Grilled steak with mashed sweet potatoes and green beans (Protein, Fiber)
        Western: Chicken Alfredo with zucchini noodles (Protein, Fiber)
        Western: Baked salmon with roasted cauliflower and quinoa (Omega-3, Protein)
        Western: Beef stir-fry with bell peppers, broccoli, and rice (Protein, Fiber)
        Western: Grilled shrimp with avocado salsa and quinoa (Omega-3, Protein)
        Western: Chicken stir-fry with mixed vegetables and quinoa (Protein, Fiber)
        Western: Vegan Buddha bowl with chickpeas, quinoa, avocado, and kale (Protein, Fiber)
        Western: Turkey burger with avocado and mixed greens (Protein, Fiber)
        Western: Chicken and vegetable skewers with quinoa (Protein, Fiber)
        Western: Grilled fish tacos with cabbage slaw and avocado (Omega-3, Protein)
        Western: Grilled steak with quinoa and roasted vegetables (Protein, Fiber)
        Western: Baked cod with roasted Brussels sprouts and sweet potatoes (Protein, Fiber)
        Western: Grilled shrimp with quinoa and roasted vegetables (Omega-3, Protein)
        Western: Vegan lentil stew with vegetables and quinoa (Fiber, Protein)
        Japanese: Ebi Tempura (shrimp tempura) with rice and miso soup (Protein, Fiber)
        Japanese: Katsu Don (breaded pork bowl) with rice (Protein, Fiber)
        Japanese: Saba Misoni (mackerel simmered in miso) with rice (Omega-3, Protein)
        Japanese: Shrimp Udon with bok choy and mushrooms (Omega-3, Protein)
        Japanese: Grilled Teriyaki chicken with sautéed vegetables (Protein, Fiber)
        Japanese: Yaki Tori (grilled chicken skewers) with rice (Protein, Fiber)
        Japanese: Unagi Don (grilled eel) with rice and vegetables (Omega-3, Protein)
        Japanese: Salmon Teriyaki with steamed rice and spinach (Omega-3, Protein)
        Japanese: Kakiage (vegetable fritters) with dipping sauce and rice (Fiber, Protein)
        Japanese: Beef Shogayaki (ginger stir-fried beef) with rice (Protein, Fiber)
        Japanese: Tofu Stir-fry with vegetables and miso sauce (Protein, Fiber)
    
    **30-39 years (Adults):**
        - Focus:
        The 30s often focus on maintaining a balanced lifestyle amidst career, family, and physical health management. The key focus is preventing health issues by making proactive choices for long-term well-being. There may also be changes in metabolism and muscle mass, which require adjustments in diet and physical activity.
        Stress management, healthy aging, and muscle preservation.
        Maintaining healthy body weight and metabolism, preventing midlife weight gain.
        Promoting mental clarity, reducing stress, and combating work-life imbalance.
        - Key Nutrients:
        Fiber: Helps manage weight, regulate blood sugar, and supports heart health.
        Protein: Vital for maintaining muscle mass and strength. This is particularly important as metabolism begins to slow in the 30s.
        Healthy Fats: Omega-3s, in particular, support brain health, inflammation reduction, and cardiovascular health.
        Antioxidants: Important for reducing oxidative stress and preventing early signs of aging, including skin and joint health.
        - Meal Suggestions:
        - **Breakfast:**
        Korean: Kimchi Pancakes (김치전) with a side of pickled vegetables (Protein, Fiber)
        Korean: Jeon (전) with zucchini, mushrooms, and egg (Protein, Fiber)
        Korean: Soondae (순대) - Korean blood sausage with vegetables (Protein, Iron)
        Korean: Mulhye (물회) - Cold raw fish soup with vegetables (Protein, Omega-3)
        Korean: Soft Boiled Egg with Gochujang and rice (Protein, Fiber)
        Western: Smoothie Bowl with spinach, berries, and chia seeds (Protein, Fiber)
        Western: Scrambled eggs with avocado and whole grain toast (Protein, Healthy Fats)
        Western: Almond butter and banana smoothie with almond milk (Protein, Fiber)
        Western: Whole grain oatmeal with flaxseed and mixed nuts (Fiber, Protein)
        Western: Protein smoothie with spinach, berries, and almond milk (Protein, Fiber)
        Western: Tofu and spinach scramble with avocado (Protein, Fiber)
        Western: Overnight oats with chia seeds, coconut milk, and mixed berries (Protein, Fiber)
        Western: Poached eggs on avocado toast with tomato (Protein, Healthy Fats)
        Western: Yogurt parfait with granola, chia seeds, and strawberries (Protein, Fiber)
        Western: Chia seed pudding with coconut milk, almonds, and strawberries (Protein, Fiber)
        Western: Spinach and mushroom frittata with quinoa (Protein, Fiber)
        Western: Protein pancakes with almond butter and blueberries (Protein, Fiber)
        Western: Greek yogurt with honey, walnuts, and mixed berries (Protein, Healthy Fats)
        Western: Whole wheat toast with almond butter, chia seeds, and banana slices (Protein, Fiber)
        Japanese: Miso soup with tofu, wakame seaweed, and green onions (Protein, Fiber)
        Japanese: Tamagoyaki (sweet Japanese omelet) with rice (Protein)
        Japanese: Japanese Pancakes (Okonomiyaki) with vegetables and pork (Protein, Fiber)
        Japanese: Chawanmushi (steamed egg custard) with shrimp and mushrooms (Protein, Fiber)
        Japanese: Teriyaki salmon with steamed rice and spinach (Omega-3, Protein)
        Japanese: Sushi rolls with tuna, avocado, and cucumber (Omega-3, Protein)
        Japanese: Katsu (breaded pork cutlet) with shredded cabbage (Protein, Fiber)
        Japanese: Edamame with a sprinkle of sea salt (Protein, Fiber)
        Japanese: Grilled mackerel with a side of miso soup (Omega-3, Protein)
        Japanese: Okonomiyaki (savory pancake) with pork belly and vegetables (Protein, Fiber)
        Japanese: Rice porridge (Okayu) with pickled vegetables (Fiber, Vitamins)
        - **Lunch:**
        Korean: Banchan (반찬) with grilled beef and vegetables (Protein, Fiber)
        Korean: Jjajangmyeon (짜장면) - Black bean paste noodles with pork (Protein, Fiber)
        Korean: Tofu Bibimbap (비빔밥) - Mixed rice with tofu and vegetables (Protein, Fiber)
        Korean: Gukbap (국밥) with pork and kimchi (Protein, Fiber)
        Korean: Oxtail Soup (꼬리곰탕) with steamed rice (Protein, Fiber)
        Western: Grilled chicken salad with mixed greens, tomatoes, and balsamic vinaigrette (Protein, Fiber)
        Western: Grilled pork chops with roasted sweet potatoes and broccoli (Protein, Fiber)
        Western: Grilled portobello mushrooms with quinoa and vegetables (Fiber, Protein)
        Western: Veggie burger with avocado and mixed greens (Protein, Fiber)
        Western: Quinoa-stuffed bell peppers with a side of mixed greens (Protein, Fiber)
        Western: Shrimp stir-fry with broccoli, carrots, and brown rice (Omega-3, Protein)
        Western: Chicken Caesar wrap with spinach (Protein, Fiber)
        Western: Grilled fish tacos with cabbage slaw and avocado (Omega-3, Protein)
        Western: Spaghetti with turkey meatballs and marinara sauce (Protein, Fiber)
        Western: Grilled shrimp with avocado and quinoa salad (Omega-3, Protein)
        Western: Grilled chicken breast with roasted potatoes and green beans (Protein, Fiber)
        Western: Quinoa bowl with roasted vegetables, chickpeas, and tahini dressing (Protein, Fiber)
        Western: Roasted chicken with mashed sweet potatoes and spinach (Protein, Fiber)
        Western: Baked salmon with roasted Brussels sprouts and quinoa (Omega-3, Protein)
        Japanese: Gyu Don (beef rice bowl) with vegetables (Protein, Fiber)
        Japanese: Tofu Katsu (breaded tofu cutlet) with rice (Protein, Fiber)
        Japanese: Teriyaki chicken with sautéed vegetables and rice (Protein, Fiber)
        Japanese: Soba noodles with tempura shrimp and vegetables (Omega-3, Protein)
        Japanese: Chicken karaage (fried chicken) with rice and miso soup (Protein, Fiber)
        Japanese: Tonkatsu (breaded pork) with steamed rice (Protein, Fiber)
        Japanese: Udon noodles with beef and onions (Protein, Fiber)
        Japanese: Grilled eel with rice and pickled vegetables (Omega-3, Protein)
        Japanese: Salmon Teriyaki with steamed vegetables and rice (Omega-3, Protein)
        Japanese: Salmon sashimi with rice and miso soup (Omega-3, Protein)
        Japanese: Sashimi platter with a variety of fish (Omega-3, Protein)
        - **Dinner:**
        Korean: Galbi (갈비) - Grilled beef short ribs with vegetables (Protein, Fiber)
        Korean: Kimchi Jjigae (김치찌개) - Kimchi stew with tofu and pork (Protein, Fiber)
        Korean: Samgyetang (삼계탕) - Ginseng chicken soup (Protein, Fiber)
        Korean: Tofu stew (두부찌개) with vegetables (Protein, Fiber)
        Korean: Pajeon (파전) - Korean savory pancake with green onions and seafood (Protein, Fiber)
        Western: Grilled chicken with roasted sweet potatoes and kale (Protein, Fiber)
        Western: Shrimp and vegetable stir-fry with brown rice (Omega-3, Protein)
        Western: Grilled steak with roasted potatoes and asparagus (Protein, Fiber)
        Western: Vegan chili with quinoa and avocado (Protein, Fiber)
        Western: Lemon herb grilled chicken with quinoa and steamed broccoli (Protein, Fiber)
        Western: Grilled chicken and vegetable kebabs with couscous (Protein, Fiber)
        Western: Baked cod with a side of quinoa and roasted vegetables (Protein, Fiber)
        Western: Grilled turkey breast with roasted Brussels sprouts and mashed potatoes (Protein, Fiber)
        Western: Baked salmon with quinoa and sautéed spinach (Omega-3, Protein)
        Western: Vegan lentil stew with mixed vegetables and quinoa (Fiber, Protein)
        Western: Baked chicken with roasted zucchini and sweet potatoes (Protein, Fiber)
        Western: Grilled shrimp with quinoa and roasted vegetables (Omega-3, Protein)
        Western: Vegan stuffed peppers with quinoa, beans, and avocado (Protein, Fiber)
        Western: Grilled lamb chops with quinoa and roasted vegetables (Protein, Fiber)
        Japanese: Shabu Shabu (hot pot) with tofu and vegetables (Protein, Fiber)
        Japanese: Unagi Don (grilled eel on rice) with pickled vegetables (Omega-3, Protein)
        Japanese: Tonkotsu Ramen (pork broth ramen) with vegetables (Protein, Fiber)
        Japanese: Chirashi Sushi (scattered sushi) with tuna and salmon (Omega-3, Protein)
        Japanese: Katsuobushi (dried bonito flakes) on rice with miso soup (Protein, Omega-3)
        Japanese: Yaki Tori (grilled chicken skewers) with steamed rice (Protein, Fiber)
        Japanese: Miso-glazed grilled mackerel with rice and spinach (Omega-3, Protein)
        Japanese: Gyoza (dumplings) with dipping sauce (Protein, Fiber)
        Japanese: Sukiyaki (beef hot pot) with tofu and vegetables (Protein, Fiber)
        Japanese: Grilled saba (mackerel) with rice and miso soup (Omega-3, Protein)
        Japanese: Vegetable tempura with rice (Fiber, Protein)
    **40-49 years (Adults):**
        - Focus:
        In the 40s, many experience changes in metabolism, muscle mass, and joint health. The key focus is to maintain a healthy weight, manage stress levels, and support healthy aging. Lifestyle choices become critical for preventing chronic conditions such as cardiovascular disease, diabetes, and joint degeneration.
        Maintaining bone density, joint health, and supporting metabolism to prevent weight gain.
        Preventing cardiovascular disease and managing cholesterol levels through healthy fats and antioxidants.
        Supporting cognitive health and mental well-being, with a focus on stress reduction.
        - Key Nutrients:
        Omega-3: Essential for reducing inflammation, supporting cardiovascular health, and improving brain function.
        Fiber: Helps reduce the risk of heart disease, manage blood sugar, and support digestive health.
        Calcium: Continues to play a significant role in bone health, helping to prevent osteoporosis.
        Protein: Important for maintaining lean muscle mass, which naturally declines with age.
        - Meal Suggestions:
        - **Breakfast:**
        Korean: Kimchi Bokkumbap (김치볶음밥) with a fried egg (Protein, Fiber)
        Korean: Juk (죽) - Rice porridge with abalone (Protein, Omega-3)
        Korean: Gyeranjjim (계란찜) - Steamed egg with vegetables (Protein, Fiber)
        Korean: Porridge with pumpkin and beans (Protein, Fiber)
        Korean: Steamed rice with grilled pork belly (Protein, Healthy Fats)
        Western: Quinoa porridge with almond butter and blueberries (Protein, Fiber)
        Western: Chia pudding with coconut milk, almonds, and mixed berries (Protein, Fiber)
        Western: Egg and avocado toast with cherry tomatoes (Protein, Healthy Fats)
        Western: Smoked salmon on whole grain toast with cucumber (Omega-3, Protein)
        Western: Scrambled eggs with spinach, tomatoes, and feta cheese (Protein, Fiber)
        Western: Green smoothie with kale, chia seeds, and almond milk (Protein, Fiber)
        Western: Whole wheat pancakes with almond butter and banana (Protein, Fiber)
        Western: Whole grain waffles with almond butter and chia seeds (Protein, Fiber)
        Western: Greek yogurt with chia seeds, honey, and granola (Protein, Fiber)
        Western: Protein-packed smoothie with peanut butter, banana, and almond milk (Protein, Healthy Fats)
        Western: Veggie-packed omelette with mushrooms, spinach, and tomatoes (Protein, Fiber)
        Western: Scrambled tofu with spinach and avocado (Protein, Fiber)
        Western: Overnight oats with chia seeds, almond milk, and strawberries (Protein, Fiber)
        Western: Breakfast burrito with eggs, spinach, and black beans (Protein, Fiber)
        Japanese: Tamago Sushi (sweet egg sushi) with cucumber (Protein, Fiber)
        Japanese: Chazuke (茶漬け) - Rice with green tea and salmon (Omega-3, Protein)
        Japanese: Nattō (fermented soybeans) with rice and pickles (Protein, Fiber)
        Japanese: Japanese yogurt with sweet red bean paste (Protein, Fiber)
        Japanese: Okonomiyaki (savory pancake) with shrimp and vegetables (Protein, Fiber)
        Japanese: Japanese rice ball (onigiri) with salmon filling (Omega-3, Protein)
        Japanese: Hiyayakko (冷やっこ) - Cold tofu with soy sauce and green onions (Protein, Fiber)
        Japanese: Shiso leaves with miso soup (Omega-3, Fiber)
        Japanese: Oyakodon (親子丼) - Chicken and egg rice bowl (Protein, Fiber)
        Japanese: Miso soup with salmon and vegetables (Omega-3, Protein)
        Japanese: Umeboshi (pickled plum) with steamed rice (Fiber, Vitamin C)
        - **Lunch:**
        Korean: Doenjang Chigae (된장찌개) with beef and tofu (Protein, Fiber)
        Korean: Kalbitang (갈비탕) - Beef short rib soup (Protein, Fiber)
        Korean: Dak Galbi (닭갈비) - Spicy stir-fried chicken with vegetables (Protein, Fiber)
        Korean: Bibim Naengmyeon (비빔냉면) - Cold spicy noodles with vegetables (Fiber, Protein)
        Korean: Samgyeopsal (삼겹살) - Grilled pork belly with kimchi (Protein, Healthy Fats)
        Western: Grilled turkey breast with quinoa salad and avocado (Protein, Fiber)
        Western: Grilled chicken Caesar salad with mixed greens (Protein, Fiber)
        Western: Veggie stir-fry with tofu and brown rice (Protein, Fiber)
        Western: Veggie and black bean taco with avocado and salsa (Protein, Fiber)
        Western: Baked chicken thighs with roasted carrots and quinoa (Protein, Fiber)
        Western: Grilled salmon with quinoa and mixed greens (Omega-3, Protein)
        Western: Grilled pork tenderloin with mashed sweet potatoes and green beans (Protein, Fiber)
        Western: Eggplant and quinoa casserole with mixed veggies (Fiber, Protein)
        Western: Grilled chicken sandwich with avocado and whole-grain bread (Protein, Healthy Fats)
        Western: Roasted vegetable and chickpea salad with tahini dressing (Fiber, Protein)
        Western: Roasted salmon with quinoa and sautéed kale (Omega-3, Protein)
        Western: Baked cod with roasted Brussels sprouts and quinoa (Protein, Fiber)
        Western: Spaghetti squash with marinara sauce and ground turkey (Protein, Fiber)
        Western: Grilled portobello mushrooms with couscous and roasted vegetables (Fiber, Protein)
        Japanese: Tonkatsu (breaded pork cutlet) with rice (Protein, Fiber)
        Japanese: Unagi Don (grilled eel with rice) and pickles (Omega-3, Protein)
        Japanese: Ramen with miso broth, tofu, and vegetables (Protein, Fiber)
        Japanese: Maki sushi with tuna and avocado (Omega-3, Protein)
        Japanese: Sukiyaki (beef hot pot) with tofu and vegetables (Protein, Fiber)
        Japanese: Teriyaki salmon with broccoli and quinoa (Omega-3, Protein)
        Japanese: Chirashi sushi (scattered sushi) with a variety of fish (Omega-3, Protein)
        Japanese: Tempura (fried vegetables) with rice (Protein, Fiber)
        Japanese: Grilled mackerel with miso soup and rice (Omega-3, Protein)
        Japanese: Udon noodles with seafood and spinach (Omega-3, Protein)
        Japanese: Bento box with grilled fish, rice, and vegetables (Omega-3, Fiber)
        - **Dinner:**
        Korean: Galbi Jjim (갈비찜) - Braised short ribs with vegetables (Protein, Fiber)
        Korean: Tofu Kimchi Jeongol (두부김치전골) - Stew with tofu and kimchi (Protein, Fiber)
        Korean: Kimchi Jeon (김치전) with rice (Protein, Fiber)
        Korean: Spicy Pork Stir-fry (제육볶음) with vegetables and rice (Protein, Fiber)
        Korean: Jangjorim (장조림) - Soy-braised beef with rice (Protein, Fiber)
        Western: Grilled lamb with quinoa and roasted vegetables (Protein, Fiber)
        Western: Grilled shrimp with garlic and quinoa (Omega-3, Protein)
        Western: Veggie lasagna with spinach and ricotta cheese (Protein, Fiber)
        Western: Roasted chicken with sweet potatoes and green beans (Protein, Fiber)
        Western: Grilled chicken skewers with roasted carrots and quinoa (Protein, Fiber)
        Western: Grilled steak with roasted potatoes and asparagus (Protein, Fiber)
        Western: Vegan chili with beans, quinoa, and avocado (Protein, Fiber)
        Western: Grilled turkey breast with roasted Brussels sprouts and mashed sweet potatoes (Protein, Fiber)
        Western: Roasted chicken with quinoa and steamed spinach (Protein, Fiber)
        Western: Baked salmon with roasted vegetables and quinoa (Omega-3, Protein)
        Western: Grilled fish tacos with cabbage and avocado (Omega-3, Protein)
        Western: Baked cod with quinoa and roasted Brussels sprouts (Protein, Fiber)
        Western: Grilled shrimp stir-fry with broccoli and rice (Omega-3, Protein)
        Western: Grilled chicken with roasted vegetables and quinoa (Protein, Fiber)
        Japanese: Yaki Udon (fried udon noodles) with vegetables and tofu (Protein, Fiber)
        Japanese: Saba Shioyaki (salt-grilled mackerel) with rice and miso soup (Omega-3, Protein)
        Japanese: Unagi Kabayaki (grilled eel) with rice and pickles (Omega-3, Protein)
        Japanese: Tonkotsu Ramen with pork and vegetables (Protein, Fiber)
        Japanese: Gyu Don (beef rice bowl) with vegetables (Protein, Fiber)
        Japanese: Grilled fish (mackerel) with miso soup and rice (Omega-3, Protein)
        Japanese: Bento box with rice, fish, and pickled vegetables (Omega-3, Fiber)
        Japanese: Okonomiyaki (savory pancake) with seafood (Protein, Fiber)
        Japanese: Teriyaki chicken with rice and sautéed vegetables (Protein, Fiber)
        Japanese: Tempura Udon with shrimp and vegetables (Protein, Fiber)
        Japanese: Chanko Nabe (sumo stew) with tofu and vegetables (Protein, Fiber)
    **50-59 years (Adults):**
        - Focus:
        In the 50s, the focus shifts toward maintaining overall health and preventing chronic diseases. Many individuals in this age group experience changes in metabolism, joint health, and energy levels. The goal is to maintain vitality, heart health, and optimal weight while managing symptoms of aging and stress.
        Supporting cardiovascular health, including managing cholesterol and blood pressure.
        Maintaining muscle strength, bone density, and joint health to remain physically active.
        Managing stress and ensuring mental clarity, which can be impacted by the aging process.
        - Key Nutrients:
        Omega-3: Supports heart health, reduces inflammation, and maintains cognitive function.
        Calcium: Key for bone strength and preventing osteoporosis, especially for post-menopausal women.
        Fiber: Crucial for maintaining digestive health, controlling blood sugar, and preventing heart disease.
        Protein: Helps to prevent muscle loss, supports healthy metabolism, and maintains overall physical strength.
        - Meal Suggestions:
        - **Breakfast:**
        Korean: Kimchi Jeon (김치전) with a boiled egg (Protein, Fiber)
        Korean: Gyeran Jjim (계란찜) with spinach and tofu (Protein, Calcium)
        Korean: Doenjang Jjigae (된장찌개) with mushrooms (Fiber, Protein)
        Korean: Oi Naengguk (오이냉국) with pickled cucumber and tofu (Fiber, Probiotics)
        Korean: Banchan (반찬) with grilled fish and rice (Omega-3, Protein)
        Western: Whole grain pancakes with almond butter and blueberries (Fiber, Healthy fats)
        Western: Quinoa and chia pudding with almond milk and honey (Fiber, Omega-3)
        Western: Scrambled eggs with avocado and mixed greens (Protein, Healthy fats)
        Western: Steel-cut oatmeal with flaxseeds, chia seeds, and almonds (Fiber, Omega-3)
        Western: Greek yogurt with walnuts and honey (Protein, Calcium)
        Western: Avocado smoothie with kale and chia seeds (Healthy fats, Fiber)
        Western: Baked eggs with spinach, mushrooms, and cheese (Protein, Calcium)
        Japanese: Tamago (Egg) sushi with rice (Protein, Fiber)
        Japanese: Miso soup with tofu and seaweed (Protein, Fiber, Calcium)
        Japanese: Onigiri (rice ball) with tuna and avocado (Omega-3, Protein)
        Japanese: Natto (fermented soybeans) with rice (Protein, Fiber, Probiotics)
        Japanese: Rice porridge (Okayu) with pickled vegetables (Fiber, Vitamins)
        Western: Smoothie bowl with berries, granola, and chia seeds (Fiber, Antioxidants)
        Western: Almond butter on whole-grain toast with banana (Healthy fats, Fiber)
        Western: Chia and flaxseed pudding with almond milk (Omega-3, Fiber)
        Western: Poached egg with avocado and tomato on whole-grain toast (Protein, Healthy fats)
        Western: Green smoothie with spinach, banana, and coconut milk (Fiber, Antioxidants)
        Korean: Tofu stew with vegetables and kimchi (Protein, Fiber)
        Korean: Juk (죽) with ginseng and mushrooms (Fiber, Antioxidants)
        Korean: Jeonbokjuk (전복죽) with abalone (Protein, Omega-3)
        Western: Cottage cheese with strawberries and walnuts (Protein, Calcium)
        Western: Baked quinoa and egg muffins with spinach (Fiber, Protein)
        Western: Protein smoothie with almond milk, spinach, and chia (Protein, Omega-3)
        Western: Whole-grain toast with poached egg, avocado, and tomato (Protein, Healthy fats)
        Western: Oatmeal with nuts, honey, and coconut flakes (Fiber, Healthy fats)
        - **Lunch:**
        Korean: Bulgogi (불고기) with quinoa and grilled vegetables (Protein, Fiber)
        Korean: Kimchi Jjigae (김치찌개) with tofu and rice (Probiotics, Protein)
        Korean: Samgyeopsal (삼겹살) with steamed broccoli (Protein, Healthy fats)
        Korean: Jajangmyeon (짜장면) with pork and vegetables (Protein, Fiber)
        Korean: Sundubu Jjigae (순두부찌개) with vegetables and tofu (Protein, Fiber)
        Western: Grilled chicken salad with kale, avocado, and walnuts (Protein, Healthy fats)
        Western: Grilled turkey and quinoa bowl with roasted vegetables (Protein, Fiber)
        Western: Roasted vegetable and chickpea salad with tahini dressing (Fiber, Protein)
        Western: Tuna salad with mixed greens, avocado, and olive oil (Omega-3, Protein)
        Western: Grilled salmon with quinoa and steamed vegetables (Omega-3, Protein)
        Western: Vegetable stir-fry with tofu and brown rice (Protein, Fiber)
        Western: Grilled vegetable wrap with hummus and falafel (Fiber, Protein)
        Japanese: Teriyaki salmon with steamed vegetables and rice (Omega-3, Protein)
        Japanese: Sashimi platter with tuna, salmon, and avocado (Omega-3, Protein)
        Japanese: Udon noodles with tofu and spinach (Protein, Fiber)
        Japanese: Tonkatsu (breaded pork) with steamed vegetables (Protein, Fiber)
        Western: Veggie burger with whole-grain bun and avocado (Fiber, Protein)
        Western: Sweet potato and black bean salad with quinoa (Fiber, Protein)
        Western: Grilled shrimp salad with avocado and cucumber (Omega-3, Protein)
        Western: Grilled chicken with roasted potatoes and green beans (Protein, Fiber)
        Korean: Grilled mackerel with steamed rice and vegetables (Omega-3, Protein)
        Korean: Grilled tofu with kimchi and quinoa (Protein, Fiber)
        Western: Chicken Caesar salad with kale (Protein, Healthy fats)
        Western: Baked falafel with hummus and tabbouleh (Protein, Fiber)
        Western: Baked salmon with roasted sweet potatoes (Omega-3, Protein)
        Western: Roasted turkey breast with quinoa and Brussels sprouts (Protein, Fiber)
        Japanese: Miso soup with tofu, seaweed, and vegetables (Protein, Fiber)
        Japanese: Grilled eel (Unagi) with rice (Omega-3, Protein)
        Korean: Bibimbap (비빔밥) with tofu and vegetables (Protein, Fiber)
        Western: Baked chicken breast with spinach and quinoa (Protein, Fiber)
        - **Dinner:**
        Korean: Galbitang (갈비탕) with rice (Protein, Calcium, Iron)
        Korean: Kimchi Bokkeumbap (김치볶음밥) with tofu and vegetables (Fiber, Protein)
        Korean: Tofu stir-fry with mushrooms and rice (Protein, Fiber)
        Korean: Doenjang Jjigae (된장찌개) with tofu and steamed vegetables (Protein, Fiber)
        Korean: Dak Galbi (닭갈비) with grilled vegetables (Protein, Fiber)
        Western: Grilled chicken breast with quinoa and steamed broccoli (Protein, Fiber)
        Western: Baked fish with mashed cauliflower and green beans (Omega-3, Protein)
        Western: Grilled lamb chops with quinoa and asparagus (Protein, Fiber)
        Western: Spaghetti with marinara sauce and turkey meatballs (Protein, Fiber)
        Western: Quinoa-stuffed bell peppers with grilled chicken (Fiber, Protein)
        Western: Baked salmon with roasted sweet potatoes (Omega-3, Protein)
        Western: Sweet potato fries with grilled turkey (Fiber, Protein)
        Western: Grilled shrimp with mixed greens and avocado (Omega-3, Protein)
        Western: Vegetable stir-fry with tofu and quinoa (Protein, Fiber)
        Western: Turkey meatloaf with roasted vegetables (Protein, Fiber)
        Japanese: Beef Sukiyaki (すき焼き) with tofu and vegetables (Protein, Fiber)
        Japanese: Grilled mackerel with steamed rice and vegetables (Omega-3, Protein)
        Japanese: Teriyaki chicken with quinoa and vegetables (Protein, Fiber)
        Korean: Banchan (반찬) with grilled fish and steamed vegetables (Omega-3, Protein)
        Korean: Grilled tofu with kimchi and quinoa (Protein, Fiber)
        Western: Grilled steak with roasted sweet potatoes and spinach (Protein, Fiber)
        Western: Spaghetti squash with marinara sauce and turkey (Protein, Fiber)
        Western: Chicken stir-fry with vegetables and brown rice (Protein, Fiber)
        Western: Grilled salmon with roasted Brussels sprouts (Omega-3, Protein)
        Korean: Grilled mackerel with kimchi and rice (Omega-3, Protein)
        Korean: Sundubu Jjigae (순두부찌개) with vegetables (Protein, Fiber)
        Japanese: Udon noodles with tofu and vegetables (Protein, Fiber)
        Japanese: Tonkotsu ramen with pork and vegetables (Protein, Fiber)
        Western: Baked chicken breast with spinach and quinoa (Protein, Fiber)
        Western: Shrimp stir-fry with quinoa and broccoli (Omega-3, Protein)
    
    **60+ years (Seniors):**
        - Focus:
        In the senior years, maintaining independence and quality of life becomes a priority. Focus is on preventing and managing chronic diseases, maintaining bone and joint health, and improving digestion. Nutrient-dense foods are crucial to ensure that the body continues to receive adequate nutrients for daily function and health maintenance.
        Maintaining muscle mass and functional strength to reduce the risk of falls and fractures.
        Supporting digestive health to counteract slower digestion and nutrient absorption.
        Focus on heart health and blood circulation to manage age-related conditions such as hypertension.
        - Key Nutrients:
        Calcium: Important for maintaining bone density and preventing fractures, especially in postmenopausal women and older men.
        Fiber: Helps manage constipation, lower cholesterol, and regulate blood sugar, which can be more challenging in older age.
        Omega-3: Reduces inflammation, supports cognitive health, and promotes cardiovascular well-being.
        Protein: Essential for maintaining muscle mass and strength, preventing sarcopenia, and supporting recovery from illness or surgery.
        - Meal Suggestions:
        - **Breakfast:**
        Korean: Tofu and vegetable stew (두부채소찌개) with rice (Protein, Calcium)
        Korean: Galbitang (갈비탕) with steamed vegetables (Protein, Calcium)
        Korean: Kimchi Jeon (김치전) with eggs (Protein, Fiber)
        Korean: Tofu and spinach stew (두부시금치국) with a side of rice (Protein, Fiber)
        Korean: Seaweed soup (미역국) with tofu and rice (Calcium, Protein)
        Western: Greek yogurt with chia seeds, flaxseeds, and walnuts (Protein, Omega-3)
        Western: Oatmeal with chia seeds, berries, and almond butter (Fiber, Omega-3)
        Western: Whole-grain toast with scrambled eggs, avocado, and spinach (Protein, Healthy fats)
        Western: Almond milk smoothie with spinach, banana, and chia seeds (Fiber, Calcium)
        Western: Scrambled eggs with tomatoes and mushrooms on whole-grain toast (Protein, Fiber)
        Western: Cottage cheese with strawberries, walnuts, and flaxseeds (Protein, Omega-3)
        Western: Overnight oats with almond milk, chia seeds, and berries (Fiber, Omega-3)
        Japanese: Miso soup with tofu and seaweed (Protein, Fiber)
        Japanese: Tamagoyaki (Japanese rolled omelet) with rice (Protein, Calcium)
        Japanese: Rice porridge (Okayu) with pickled vegetables (Fiber, Probiotics)
        Japanese: Rice and natto (fermented soybeans) (Protein, Probiotics)
        Japanese: Grilled fish (such as mackerel) with rice and miso soup (Omega-3, Protein)
        Western: Chia pudding with almond milk and mixed berries (Fiber, Omega-3)
        Western: Smoothie bowl with berries, almond butter, and granola (Fiber, Protein)
        Western: Avocado toast with poached eggs and arugula (Healthy fats, Protein)
        Western: Poached eggs with spinach and mushrooms (Protein, Calcium)
        Western: Green smoothie with kale, cucumber, and lemon (Fiber, Antioxidants)
        Korean: Kimchi with steamed tofu (Probiotics, Protein)
        Korean: Oatmeal with soy milk, walnuts, and chia seeds (Fiber, Omega-3)
        Western: Protein smoothie with almond milk, spinach, and chia seeds (Protein, Omega-3)
        Western: Quinoa and chia pudding with almond milk and honey (Fiber, Omega-3)
        Western: Scrambled eggs with smoked salmon and spinach (Omega-3, Protein)
        Western: Whole grain pancakes with blueberries and honey (Fiber, Antioxidants)
        Western: Oatmeal with flaxseeds, chia seeds, and almond butter (Fiber, Omega-3)
        Western: Greek yogurt parfait with granola, walnuts, and berries (Protein, Omega-3)
        - **Lunch:**
        Korean: Bulgogi (불고기) with steamed rice and vegetables (Protein, Fiber)
        Korean: Doenjang Jjigae (된장찌개) with tofu and mushrooms (Protein, Fiber)
        Korean: Grilled fish (mackerel) with steamed broccoli and rice (Omega-3, Protein)
        Korean: Samgyeopsal (삼겹살) with kimchi and grilled vegetables (Protein, Fiber)
        Korean: Chicken Bibimbap (비빔밥) with assorted vegetables (Protein, Fiber)
        Western: Grilled chicken salad with avocado, spinach, and walnuts (Protein, Healthy fats)
        Western: Grilled salmon with quinoa and steamed vegetables (Omega-3, Protein)
        Western: Turkey wrap with avocado, lettuce, and tomatoes (Protein, Healthy fats)
        Western: Roasted vegetable quinoa salad with chickpeas (Fiber, Protein)
        Western: Veggie burger with avocado and spinach on whole-grain bun (Protein, Fiber)
        Western: Grilled shrimp with mixed greens and avocado (Omega-3, Protein)
        Western: Grilled chicken with roasted sweet potatoes and kale (Protein, Fiber)
        Japanese: Teriyaki salmon with sautéed spinach and rice (Omega-3, Protein)
        Japanese: Sushi rolls with avocado and cucumber (Omega-3, Fiber)
        Japanese: Tofu stir-fry with broccoli and bell peppers (Protein, Fiber)
        Japanese: Grilled eel (Unagi) with rice (Omega-3, Protein)
        Japanese: Sashimi (tuna, salmon) with miso soup (Omega-3, Protein)
        Western: Spinach and feta stuffed chicken breast with quinoa (Protein, Fiber)
        Western: Sweet potato and black bean salad with quinoa (Fiber, Protein)
        Western: Grilled turkey burger with a side of mixed greens (Protein, Fiber)
        Western: Baked cod with roasted cauliflower and quinoa (Protein, Fiber)
        Western: Roasted vegetable and chickpea bowl with tahini dressing (Fiber, Protein)
        Korean: Grilled mackerel with quinoa and kimchi (Omega-3, Protein)
        Korean: Galbi (갈비) with grilled vegetables (Protein, Calcium)
        Korean: Spicy tofu stew with spinach and mushrooms (Protein, Fiber)
        Western: Baked chicken with roasted sweet potatoes and asparagus (Protein, Fiber)
        Western: Quinoa-stuffed bell peppers with grilled shrimp (Fiber, Omega-3)
        Western: Grilled chicken with avocado and quinoa salad (Protein, Healthy fats)
        Western: Grilled salmon with lemon butter and steamed spinach (Omega-3, Protein)
        Western: Mediterranean chicken bowl with hummus and vegetables (Protein, Fiber)
        - **Dinner:**
        Korean: Dak Jjim (닭찜) with sweet potatoes and steamed vegetables (Protein, Fiber)
        Korean: Banchan (반찬) with grilled fish and rice (Omega-3, Protein)
        Korean: Doenjang Jjigae (된장찌개) with tofu and vegetables (Protein, Fiber)
        Korean: Grilled mackerel with steamed rice and spinach (Omega-3, Protein)
        Korean: Grilled tofu with kimchi and steamed broccoli (Protein, Fiber)
        Western: Grilled lamb chops with quinoa and green beans (Protein, Fiber)
        Western: Baked salmon with roasted cauliflower and quinoa (Omega-3, Protein)
        Western: Grilled chicken breast with roasted potatoes and mixed greens (Protein, Fiber)
        Western: Spaghetti with marinara sauce and turkey meatballs (Protein, Fiber)
        Western: Quinoa-stuffed bell peppers with grilled chicken (Fiber, Protein)
        Western: Grilled shrimp stir-fry with quinoa and mixed vegetables (Omega-3, Protein)
        Western: Baked cod with roasted Brussels sprouts and quinoa (Protein, Fiber)
        Western: Grilled turkey burger with a side of sweet potato fries (Protein, Fiber)
        Western: Grilled steak with roasted vegetables and quinoa (Protein, Fiber)
        Japanese: Beef Sukiyaki (すき焼き) with tofu and vegetables (Protein, Fiber)
        Japanese: Grilled fish (mackerel) with miso soup (Omega-3, Protein)
        Japanese: Teriyaki chicken with quinoa and roasted vegetables (Protein, Fiber)
        Japanese: Udon noodles with tofu and spinach (Protein, Fiber)
        Japanese: Tonkatsu (breaded pork) with steamed broccoli (Protein, Fiber)
        Western: Baked chicken with roasted sweet potatoes and green beans (Protein, Fiber)
        Western: Grilled steak with quinoa and roasted vegetables (Protein, Fiber)
        Western: Baked turkey breast with Brussels sprouts (Protein, Fiber)
        Western: Grilled shrimp with garlic and quinoa (Omega-3, Protein)
        Western: Grilled chicken with quinoa and steamed broccoli (Protein, Fiber)
        Western: Sweet potato and kale salad with chickpeas and quinoa (Fiber, Protein)
        Korean: Kimchi Jjigae (김치찌개) with tofu and rice (Probiotics, Protein)
        Korean: Grilled fish with steamed rice and kimchi (Omega-3, Protein)
        Korean: Jajangmyeon (짜장면) with pork and vegetables (Protein, Fiber)
        Korean: Samgyetang (삼계탕) with ginseng and chicken (Protein, Fiber)
        Korean: Grilled tofu with mushrooms and vegetables (Protein, Fiber)
        
        
    - **Diet Status Adjustments:**
        - Determining Diet Status: The user's diet status can be identified using the variable {is_on_diet}, which can have two possible values:
        - **On a diet:** The user is focused on maintaining a specific weight goal or following a health regimen such as calorie reduction, fat loss, or muscle gain.
            - On a Diet: If the user is on a diet, the primary goal is typically weight loss, muscle definition, or improved metabolic health. For these purposes, the meal recommendations should prioritize:
            - Low-calorie, high-protein meals to support muscle repair, minimize fat storage, and keep the user feeling satiated longer.
            - High-fiber foods that aid in digestion, improve gut health, and contribute to feelings of fullness, thus preventing overeating.
            - Healthy fats like those found in avocados, nuts, and seeds to support hormone production and satiety.
            Recommended Meal Characteristics:=
            - Protein: Protein is essential for muscle repair and growth. Meals should contain lean sources of protein such as chicken breast, fish (especially fatty fish like salmon for omega-3s), eggs, or plant-based proteins like tofu and legumes. The goal is 20-30 grams of protein per meal.
            - Fiber: Fiber-rich foods such as vegetables, whole grains (like quinoa or brown rice), and legumes (lentils, chickpeas) help improve digestion, regulate blood sugar, and keep you full between meals. Aim for 5-10 grams of fiber per meal.
            - Healthy Fats: Healthy fats are crucial for maintaining metabolic rate and ensuring nutrient absorption. Foods like avocado, olive oil, nuts, and seeds should be incorporated in moderation, aiming for about 10-15 grams of fat per meal.
            - Low Glycemic Index: Avoid foods with a high glycemic index (e.g., white bread, sugary snacks), as they can lead to blood sugar spikes and crashes. Instead, focus on complex carbohydrates that release energy slowly.
            - Portion Control: Since the goal is weight loss or maintenance, portion control is vital. Meals should be filling but lower in calorie density, so that the user can enjoy a satisfying portion without overconsuming calories.
        - **Not on a diet:** The user is not specifically restricting calories or following any formal dietary regimen. They may focus on a balanced, healthy approach to eating, with diverse ingredients and overall well-being in mind.
            - Not on a Diet:
            - If the user is not on a diet, the focus should shift to providing a well-rounded, balanced diet that supports overall health and well-being, rather than weight loss or muscle gain. The goal here is to ensure the body receives a variety of nutrients, while still promoting optimal health.
            Recommended Meal Characteristics:
            - Balanced Macronutrients: Meals should include a healthy balance of protein, carbohydrates, and fats. This will support energy levels, muscle maintenance, and overall bodily function.
            - Micronutrient-Rich Foods: Emphasize a wide variety of fruits, vegetables, and whole grains to ensure the intake of essential vitamins and minerals. Consider the inclusion of leafy greens (e.g., kale, spinach), cruciferous vegetables (e.g., broccoli, cauliflower), and fruits high in antioxidants (e.g., berries, citrus fruits).
            - Moderate Portions: While portion control may not be as strict as for those on a diet, it is still important to eat in moderation. The focus should be on wholesome, nutrient-dense foods, with fewer processed options.
            - Carbohydrates for Energy: Complex carbohydrates such as whole grains, starchy vegetables, and legumes should make up a substantial portion of the meal. These provide steady energy release and support physical activity throughout the day.
            - Inclusion of Healthy Fats: Moderate amounts of healthy fats, such as those from nuts, seeds, olive oil, and fatty fish, are important for brain function and cell health.
        - Additional Notes:
            Hydration:
            Both for individuals on a diet and not, staying hydrated is crucial. Water plays an essential role in digestion, nutrient absorption, and energy levels. Consider recommending herbal teas or water-rich fruits (like cucumbers or watermelon) throughout the day.
            Meal Timing:
            For those on a diet, focusing on meal frequency may be helpful. Some individuals prefer eating smaller meals throughout the day to manage hunger and blood sugar levels. On the other hand, those not on a diet may find it beneficial to focus on 3 larger, balanced meals with snacks in between.
            Lifestyle Factors:
            Additional factors like exercise, sleep quality, and stress management can significantly influence the effectiveness of diet plans. For users who are active, a higher protein intake is beneficial for muscle repair. For those with high-stress levels, foods rich in magnesium (like spinach, nuts, and seeds) and omega-3s (from fatty fish) are helpful for reducing stress hormones.
    - **Example Recommendations:**
        - Describe the nutrient composition (protein, fat, carbohydrates) and health benefits (muscle recovery, blood sugar control, heart health) of each meal.
        - Explain how each ingredient helps the user achieve their dietary goals.

    Example of whole format: 
    ### If the user ate the meal at lunch, considering what user ate for breakfast({breakfast_time}), you must recommend for dinner
    Full example:
    아침에 먹은 음식: 김치 찌개
    점심에 먹은 음식: 피자 반 판
    점심 먹은 시간: 오후 1시
    
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
    
    ### 5. 저녁 식사 추천***please consider the variety of food***
    - **메뉴**: 잡곡밥, 연어구이, 나물 반찬(고사리, 무나물), 청국장, 과일(사과, 블루베리)
    잡곡밥: 복합 탄수화물로 에너지를 공급하고 섬유질이 풍부합니다.
    연어구이: 고품질 단백질과 오메가-3 지방산으로 심혈관 건강과 뇌 기능 강화에 도움을 줍니다.
    나물 반찬: 고사리와 무나물은 철분, 칼륨, 비타민 A를 보충하며 소화 기능을 돕습니다.
    청국장: 발효 식품으로 장 건강을 지원하고 단백질과 미네랄 섭취를 보완합니다.
    과일: 사과와 블루베리는 비타민 C와 항산화 물질이 풍부해 면역력 강화와 노화 방지에 효과적입니다.
    
    ### 총 영양 성분
    칼로리: 약 600kcal
    단백질: 약 45g
    연어(30g), 청국장(10g), 잡곡밥(5g)
    지방: 약 20g
    연어(15g), 청국장(5g)
    탄수화물: 약 80g
    잡곡밥(60g), 과일(20g)
    미세 영양소:
    칼슘: 나물 반찬, 청국장
    비타민 A: 고사리
    비타민 C: 과일(사과, 블루베리)
    오메가-3 지방산: 연어
    
    ### 왜 이 식사를 추천하는가?
    영양 균형 보완:
    아침(김치찌개)과 점심(피자 반 판)의 섭취 내용을 분석한 결과, 섬유질, 고품질 단백질, 오메가-3 지방산, 비타민 C가 부족했습니다. 이 메뉴는 이를 효과적으로 보충합니다.
    저녁은 하루의 총 칼로리를 적절히 맞추기 위해 600kcal로 조정되었으며, 과도한 칼로리 섭취를 방지하기 위해 설계되었습니다. 저녁은 소화가 쉬운 음식을 포함해 편안한 수면을 유도해야 합니다. 청국장과 나물 반찬은 저녁 식사로 적합하며, 장 건강과 소화 개선에 도움을 줍니다.
    
    ### 건강 이점
    잡곡밥: 복합 탄수화물이 천천히 소화되어 혈당을 안정적으로 유지하고, 하루의 에너지를 보충합니다.
    연어구이: 오메가-3 지방산은 심혈관 건강을 강화하고, 뇌 기능을 촉진합니다. 고품질 단백질은 근육 회복과 유지에 필수적입니다.
    나물 반찬: 고사리는 철분과 칼륨을 제공해 빈혈 예방과 혈압 조절에 도움을 줍니다. 무나물은 섬유질이 풍부해 소화를 돕고 장 건강을 지원합니다.
    청국장: 장내 유익균을 늘려 소화와 면역력을 강화합니다. 단백질과 미네랄이 부족한 영양소를 보충합니다.
    과일(사과, 블루베리): 항산화 물질이 풍부해 세포 노화를 방지하며, 비타민 C는 면역력 강화를 돕습니다.
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
#받는 값 없는 저녁 함수
def dinner_calculator():
    global output
    time = '저녁'
    response = input('저녁으로는 무엇을 드셨나요?: ')
    breakfast_time = input('아침으로는 무엇을 드셨나요?: ')
    launch_time = input('점심으로는 무엇을 드셨나요?: ')
    food_time = input('혹시 저녁은 몇시에 드셨나요?: ')
    age = input('현재 나이가 어떻게 되시죠?: ')
    is_on_diet = input('현재 다이어트 중이신가요?: ')
    completion = client.chat.completions.create(
    model = 'gpt-4o-mini',
    messages = [
    {'role':'system', 'content': """
    You are chef who knows all types of the food and also a professional nutrition assistant providing dietary analysis and personalized meal recommendations to users.
    ***Your primary task is to strictly adhere to the following structure while providing a comprehensive and detailed analysis. Ensure that you include variable types for each food item mentioned, categorizing them accurately and elaborating on their characteristics. Additionally, consider a variety of cuisines—Korean, Western, Chinese, and Japanese—when recommending foods or meals, highlighting their unique qualities, cultural significance, and nutritional profiles. Focus on delivering rich, in-depth information that goes beyond basic descriptions for all meals.***
    ***All responses must be written in Korean.***
    ## **Guidelines for Tasks**
    ### 1. **Dietary Analysis**
    - Analyze the key nutrients (proteins, carbohydrates, fats) and micronutrients (vitamins, minerals) of the food({response}) consumed by the user.
    - ***Explain how each food impacts the user's health based on their age ({age}) and dietary status ({is_on_diet}).***
    - Identify the user's **remaining daily nutrient requirements** and provide recommendations accordingly.
    - Describe how the food contributes to the user's health and aligns with their daily nutritional goals.
    - If a food item is unhealthy or excessive (e.g., high in calories, fats, or sugars), clearly state its potential negative effects, such as weight gain, heart disease risks, or other health concerns.
    - Avoid sugar-coating negative aspects and ensure clarity in the consequences of overconsumption.

    ### 2. **Personalized Meal Recommendations**
    - ***recommend meals from various cuisines. The cuisines to consider are Korean, Western, Chinese, and Japanese. Please ensure the recommended meal***
    - Use the user's age and dietary goals (e.g., calorie deficit for weight loss or nutrient balance for general health) to create specific meal plans for their next meal(s).
    - Ensure menus align with the user's dietary preferences and caloric goals (e.g., low-calorie, high-protein options for dieting).
    - Provide detailed explanations for why each dish or ingredient was chosen in terms of health benefits and nutritional value.
    - If a meal is recommended after the user has eaten a heavy meal (e.g., a pizza, hamburger or any food that has high calories), highlight the importance and calories of balancing nutrients (e.g., lower-calorie options, high fiber, etc.) to prevent overconsumption.
    - **Scenario: Dinner Consumed**
        - Since user ate the meal at dinner({time}), you must consider three factors which are breakfast({breakfast_time}), lunch({launch_time}) and what user ate({response}) at dinner then recommend the meal for the next day's breakfast.
        - Recommend a **next-day breakfast menu** based on the nutritional balance of breakfast, lunch, and dinner from the previous day.
        - Ensure the breakfast supports energy for the new day while maintaining nutrient balance and why the meal should be eaten at that time.
        - Explain **how the next day's breakfast menu completes their nutritional profile base on the breakfast, lunch and dinner** for the last day and why the meal should be eaten at that time.
        - You must consider or summarize the whole calories and nutrition of breakfast, lunch and dinner, then give the best solution(menu) for next day's breakfast

    ### **Consideration of Previous Meals:**
    - Always consider the **previous meals the user has consumed** when making new meal recommendations. For example, if the user has already consumed a heavy breakfast (e.g., high in calories or fats), recommend lighter meals for lunch or dinner to balance the overall daily intake.
    - After **dinner consumption**, recommend a breakfast menu for the next day that maintains a balanced nutrient profile, avoiding excess intake from the previous day.

    ### **Analysis and Recommendation Guidelines**
    **Age-Specific Adjustments**:
    - You will know how old the user is by {age}.
    **10-19 years (Adolescence):**
        - Focus:
        Adolescence is a critical period for physical and cognitive development. During this stage, the body undergoes rapid growth, with significant changes in height, muscle mass, and bone density. Nutrient needs increase to support growth, hormonal changes, and the development of a strong immune system.
        Growth and physical development, including bone health, muscle mass, and brain function.
        Hormonal balance and metabolic regulation to support puberty and increased physical activity.
        Enhanced cognitive development and memory, requiring proper nutrition for brain function.
        - Key Nutrients:
        Protein: Crucial for muscle development and tissue growth. Protein is necessary for building and repairing muscles, especially with increased physical activity.
        Calcium: Essential for developing strong, healthy bones and teeth, helping to maximize bone mass during adolescence when bone density is rapidly increasing.
        Iron: Necessary for the increased blood volume and red blood cell production during growth. It's particularly important for girls as they enter menstruation.
        Fiber: Promotes digestion, helps maintain blood sugar levels, and supports overall gut health.
        - Meal Suggestions:
        - **Breakfast:**
        Korean: Kimchi Jeon (김치전) with a side of tofu and kimchi (Fiber, Protein, Probiotics)
        Korean: Gyeran Jjim (계란찜) with steamed rice (Protein, Calcium)
        Korean: Bibimbap (비빔밥) with egg (Protein, Fiber, Vitamins)
        Korean: Tofu and vegetable stir-fry with rice (Protein, Fiber)
        Korean: Grilled mackerel with rice and kimchi (Omega-3, Protein, Fiber)
        Western: Scrambled eggs with spinach and whole-grain toast (Protein, Fiber, Iron)
        Western: Oatmeal with mixed berries and almonds (Fiber, Antioxidants)
        Western: Greek yogurt with honey and granola (Calcium, Protein)
        Western: Smoothie with banana, spinach, and protein powder (Fiber, Protein)
        Western: Whole-grain pancakes with fresh fruit (Fiber, Antioxidants)
        Western: Avocado toast with a poached egg (Healthy fats, Protein)
        Western: Chia pudding with almond milk and strawberries (Fiber, Antioxidants)
        Japanese: Tamago Sushi (Egg sushi) with rice (Protein, Fiber)
        Japanese: Miso soup with tofu and seaweed (Protein, Fiber, Calcium)
        Japanese: Natto (fermented soybeans) with rice (Protein, Probiotics, Fiber)
        Japanese: Onigiri (rice balls) with tuna and seaweed (Protein, Fiber)
        Japanese: Rice porridge (Okayu) with pickled vegetables (Fiber, Vitamins)
        Western: Whole-grain English muffin with avocado and poached egg (Healthy Fats, Protein)
        Western: Cottage cheese with pineapple and flax seeds (Protein, Fiber)
        Western: Fruit salad with chia seeds and yogurt (Fiber, Calcium)
        Western: Peanut butter on whole-grain toast with banana (Protein, Fiber)
        Korean: Galbitang (갈비탕) with rice (Protein, Calcium, Iron)
        Korean: Juk (죽) with vegetables and egg (Protein, Fiber, Calcium)
        Korean: Seaweed soup (미역국) with rice and tofu (Calcium, Protein)
        Western: Protein smoothie with oats, peanut butter, and banana (Protein, Fiber)
        Western: Apple cinnamon overnight oats (Fiber, Antioxidants)
        Western: Whole wheat bagel with cream cheese and smoked salmon (Protein, Omega-3)
        Western: Breakfast burrito with scrambled eggs and veggies (Protein, Fiber)
        Japanese: Grilled fish with rice and miso soup (Omega-3, Protein, Fiber)
        Korean: Hotteok (호떡) filled with honey and nuts (Fiber, Healthy Fats)
        Lunch:
        Korean: Bulgogi (불고기) with steamed rice and vegetables (Protein, Iron, Fiber)
        Korean: Kimchi Jjigae (김치찌개) with tofu and rice (Protein, Fiber, Probiotics)
        Korean: Bibimbap (비빔밥) with beef and egg (Protein, Fiber, Vitamins)
        Korean: Galbitang (갈비탕) with rice (Protein, Calcium, Iron)
        Korean: Grilled fish with sautéed vegetables and rice (Omega-3, Protein, Fiber)
        Western: Grilled chicken Caesar salad (Protein, Fiber, Healthy Fats)
        Western: Spaghetti with meatballs and spinach (Protein, Iron, Calcium)
        Western: Quinoa salad with chickpeas and vegetables (Fiber, Antioxidants)
        Western: Grilled chicken sandwich with whole grain bread (Protein, Fiber)
        Western: Turkey wrap with lettuce, tomato, and avocado (Protein, Healthy Fats, Fiber)
        Western: Beef stew with carrots and potatoes (Protein, Fiber, Iron)
        Western: Grilled shrimp with quinoa and roasted vegetables (Protein, Fiber)
        Japanese: Teriyaki chicken with steamed vegetables (Protein, Fiber)
        Japanese: Sushi with tuna, avocado, and cucumber (Omega-3, Protein)
        Japanese: Ramen with pork and vegetables (Protein, Fiber)
        Japanese: Donburi (rice bowl) with chicken and vegetables (Protein, Fiber)
        Japanese: Tempura with shrimp and vegetables (Protein, Fiber)
        Western: Grilled salmon with couscous and vegetables (Omega-3, Protein, Fiber)
        Western: Sweet potato and black bean burrito (Fiber, Protein, Iron)
        Western: Hummus with veggies and whole-grain pita (Fiber, Protein)
        Western: Chicken and vegetable stir-fry with brown rice (Protein, Fiber)
        Korean: Kimchi Bokkeumbap (김치볶음밥) with egg (Protein, Fiber, Probiotics)
        Korean: Tofu stir-fry with broccoli and carrots (Protein, Fiber)
        Korean: Jajangmyeon (짜장면) with vegetables and pork (Protein, Fiber)
        Western: Baked sweet potato with black beans and avocado (Fiber, Protein)
        Western: Baked salmon with mashed potatoes and broccoli (Omega-3, Protein, Fiber)
        Western: Quinoa and grilled vegetable bowl (Fiber, Protein, Antioxidants)
        Japanese: Sushi with eel and avocado (Protein, Omega-3)
        Japanese: Sashimi with tuna and salmon (Omega-3, Protein)
        Korean: Soondubu Jjigae (순두부찌개) with rice (Protein, Calcium)
        Dinner:
        Korean: Kimchi Jjigae (김치찌개) with rice (Protein, Fiber, Probiotics)
        Korean: Jjimdak (찜닭) with rice (Protein, Fiber, Iron)
        Korean: Banchan (반찬) with grilled fish and rice (Omega-3, Protein)
        Korean: Doenjang Jjigae (된장찌개) with tofu and vegetables (Fiber, Protein)
        Korean: Gimbap (김밥) with tuna and vegetables (Protein, Fiber)
        Western: Grilled steak with quinoa and broccoli (Protein, Fiber)
        Western: Salmon fillet with roasted sweet potatoes (Omega-3, Protein)
        Western: Chicken stir-fry with mixed vegetables (Protein, Fiber)
        Western: Zucchini noodles with marinara sauce and turkey meatballs (Fiber, Protein)
        Western: Grilled chicken breast with kale and quinoa salad (Protein, Fiber)
        Western: Turkey chili with kidney beans (Protein, Fiber, Iron)
        Western: Baked chicken with mashed cauliflower (Protein, Fiber)
        Japanese: Teriyaki salmon with steamed vegetables (Omega-3, Protein)
        Japanese: Miso soup with tofu and rice (Protein, Fiber)
        Japanese: Chicken Katsu (カツ) with cabbage and rice (Protein, Fiber)
        Japanese: Beef Sukiyaki (すき焼き) with tofu and vegetables (Protein, Fiber)
        Japanese: Tonkotsu ramen with pork and vegetables (Protein, Fiber)
        Western: Beef and vegetable stew (Protein, Fiber)
        Western: Grilled vegetable pasta with pesto sauce (Fiber, Healthy Fats)
        Western: Spaghetti squash with marinara sauce and grilled chicken (Fiber, Protein)
        Western: Eggplant parmesan with quinoa (Fiber, Protein, Antioxidants)
        Western: Roast chicken with Brussels sprouts and mashed potatoes (Protein, Fiber)
        Korean: Samgyeopsal (삼겹살) with grilled vegetables (Protein, Healthy Fats)
        Korean: Kimchi Bokkeumbap (김치볶음밥) with a side of vegetables (Fiber, Probiotics)
        Korean: Dak Galbi (닭갈비) with rice (Protein, Fiber)
        Japanese: Grilled eel (Unagi) with rice (Omega-3, Protein)
        Japanese: Gyoza (Japanese dumplings) with dipping sauce (Protein, Fiber)
        Western: Grilled turkey burger with avocado (Protein, Healthy Fats)
        Western: Vegetable stir-fry with tofu (Protein, Fiber)
        Western: Grilled lamb chops with sautéed spinach (Protein, Iron, Fiber)
        
    **20-29 years (Young Adults):**
        - Focus:
        This age group is marked by increased independence and stability in terms of growth and development. The primary focus is on maintaining optimal health while adapting to increased responsibilities, physical activity, and dietary habits. This phase often involves the transition into more consistent routines for fitness, career, and relationships.
        Building a healthy foundation for metabolism and body composition.
        Maintaining muscle mass and overall physical strength, often with active lifestyles or exercise routines.
        Managing stress, sleep patterns, and balancing work-life commitments for mental and emotional health.
        - Key Nutrients:
        Protein: Vital for muscle maintenance and repair, especially with physical activity and strength-building exercises.
        Fiber: Supports digestive health, regulates bowel movements, and stabilizes blood sugar levels.
        Healthy Fats: Essential for hormonal balance, brain function, and cardiovascular health.
        Antioxidants: Help protect cells from oxidative damage and support skin, eye, and overall immune system health.
        - Meal Suggestions:
        - **Breakfast:**
        Korean: Gukbap (국밥) - Hot soup with rice (Protein, Fiber)
        Korean: Kimchi Jeongol (김치전골) - Kimchi stew (Protein, Fiber)
        Korean: Tofu Jorim (두부조림) - Braised tofu (Protein, Fiber)
        Korean: Juk (죽) - Rice porridge with vegetables (Fiber, Vitamins)
        Korean: Banchan (반찬) with steamed rice and egg (Protein, Fiber)
        Western: Avocado and tomato salad on whole wheat toast (Protein, Fiber, Healthy Fats)
        Western: Banana and peanut butter smoothie with almond milk (Protein, Fiber, Healthy Fats)
        Western: Veggie scramble with mushrooms, spinach, and quinoa (Protein, Fiber)
        Western: Cottage cheese with pineapple and chia seeds (Protein, Fiber, Healthy Fats)
        Western: Whole grain toast with hummus and cucumber (Protein, Fiber)
        Western: Oats with almond butter, strawberries, and chia seeds (Protein, Fiber)
        Western: Greek yogurt with granola, blueberries, and flaxseeds (Protein, Fiber, Omega-3)
        Western: Avocado smoothie with almond milk, spinach, and chia seeds (Healthy Fats, Fiber)
        Western: Overnight oats with coconut yogurt and mixed berries (Fiber, Protein)
        Western: Whole grain waffles with almond butter and banana (Protein, Fiber)
        Western: Scrambled eggs with spinach and roasted tomatoes (Protein, Fiber)
        Western: Chia pudding with mixed nuts, coconut yogurt, and dried fruit (Fiber, Protein)
        Western: Green smoothie with kale, mango, and almond milk (Fiber, Vitamins)
        Western: Apple slices with almond butter and flaxseeds (Healthy Fats, Fiber)
        Japanese: Onigiri (rice ball) with salmon and pickled plum (Protein, Omega-3)
        Japanese: Natto (fermented soybeans) with steamed rice (Protein, Fiber)
        Japanese: Katsuobushi (dried bonito flakes) with miso soup (Protein, Omega-3)
        Japanese: Tamago Sushi (sweet egg sushi) with pickled ginger (Protein)
        Japanese: Okonomiyaki (savory pancake) with cabbage and pork (Protein, Fiber)
        Japanese: Chawanmushi (steamed egg custard) with shrimp (Protein, Fiber)
        Japanese: Miso soup with seaweed and tofu (Protein, Fiber)
        Japanese: Tofu Katsu (breaded tofu cutlet) with rice (Protein, Fiber)
        Japanese: Zosui (rice soup) with vegetables and chicken (Protein, Fiber)
        Japanese: Daifuku (mochi) with sweet red bean paste (Protein, Fiber)
        Japanese: Salmon sashimi with soy sauce and wasabi (Omega-3, Protein)
        - **Lunch:**
        Korean: Galbi Jjim (갈비찜) - Braised short ribs (Protein, Iron)
        Korean: Kimchi Bokkeumbap (김치볶음밥) - Kimchi fried rice (Protein, Fiber)
        Korean: Bulgogi (불고기) - Grilled beef with vegetables (Protein, Fiber)
        Korean: Gimbap (김밥) - Korean sushi rolls with vegetables and beef (Protein, Fiber)
        Korean: Kimchi Chigae (김치찌개) - Kimchi stew with pork (Protein, Fiber)
        Western: Grilled chicken Caesar salad with quinoa and greens (Protein, Fiber)
        Western: Grilled lamb with couscous and roasted vegetables (Protein, Fiber)
        Western: Vegan chickpea salad with avocado and mixed greens (Protein, Fiber)
        Western: Baked cod with brown rice and roasted carrots (Protein, Fiber)
        Western: Veggie wrap with hummus, avocado, and quinoa (Protein, Fiber)
        Western: Grilled turkey breast with roasted sweet potatoes and spinach (Protein, Fiber)
        Western: Grilled tofu and vegetable skewers with quinoa (Protein, Fiber)
        Western: Spaghetti with grilled vegetables and marinara sauce (Protein, Fiber)
        Western: Roast chicken with quinoa, steamed broccoli, and sweet potatoes (Protein, Fiber)
        Western: Tuna and avocado salad with mixed greens and quinoa (Protein, Fiber)
        Western: Grilled shrimp with quinoa, mixed vegetables, and lemon (Omega-3, Protein)
        Western: Vegan burrito with black beans, rice, avocado, and salsa (Protein, Fiber)
        Western: Baked chicken with roasted zucchini and quinoa (Protein, Fiber)
        Western: Turkey meatballs with zucchini noodles and marinara sauce (Protein, Fiber)
        Western: Shrimp stir-fry with rice noodles and vegetables (Omega-3, Protein)
        Japanese: Tonkotsu Ramen (pork broth ramen) with boiled egg (Protein, Fiber)
        Japanese: Gyu Don (beef rice bowl) with vegetables (Protein, Fiber)
        Japanese: Chirashi Sushi (scattered sushi) with sashimi (Protein, Omega-3)
        Japanese: Grilled mackerel with daikon radish and rice (Omega-3, Protein)
        Japanese: Tempura (battered shrimp and vegetables) with rice (Protein, Fiber)
        Japanese: Bento Box with rice, grilled salmon, and pickled vegetables (Protein, Omega-3)
        Japanese: Unagi Don (grilled eel on rice) with vegetables (Omega-3, Protein)
        Japanese: Maki Sushi with tuna and cucumber (Omega-3, Protein)
        Japanese: Shabu Shabu (hot pot) with tofu and vegetables (Protein, Fiber)
        Japanese: Teriyaki salmon with steamed rice and bok choy (Omega-3, Protein)
        - **Dinner:**
        Korean: Banchan with kimchi, tofu, and rice (Protein, Fiber)
        Korean: Samgyeopsal (삼겹살) - Grilled pork belly with vegetables (Protein, Healthy Fats)
        Korean: Jeyuk Bokkeum (제육볶음) - Spicy stir-fried pork (Protein, Fiber)
        Korean: Japchae (잡채) - Stir-fried glass noodles with beef and vegetables (Protein, Fiber)
        Korean: Galbitang (갈비탕) - Short rib soup with vegetables (Protein, Fiber)
        Western: Grilled steak with mashed sweet potatoes and green beans (Protein, Fiber)
        Western: Chicken Alfredo with zucchini noodles (Protein, Fiber)
        Western: Baked salmon with roasted cauliflower and quinoa (Omega-3, Protein)
        Western: Beef stir-fry with bell peppers, broccoli, and rice (Protein, Fiber)
        Western: Grilled shrimp with avocado salsa and quinoa (Omega-3, Protein)
        Western: Chicken stir-fry with mixed vegetables and quinoa (Protein, Fiber)
        Western: Vegan Buddha bowl with chickpeas, quinoa, avocado, and kale (Protein, Fiber)
        Western: Turkey burger with avocado and mixed greens (Protein, Fiber)
        Western: Chicken and vegetable skewers with quinoa (Protein, Fiber)
        Western: Grilled fish tacos with cabbage slaw and avocado (Omega-3, Protein)
        Western: Grilled steak with quinoa and roasted vegetables (Protein, Fiber)
        Western: Baked cod with roasted Brussels sprouts and sweet potatoes (Protein, Fiber)
        Western: Grilled shrimp with quinoa and roasted vegetables (Omega-3, Protein)
        Western: Vegan lentil stew with vegetables and quinoa (Fiber, Protein)
        Japanese: Ebi Tempura (shrimp tempura) with rice and miso soup (Protein, Fiber)
        Japanese: Katsu Don (breaded pork bowl) with rice (Protein, Fiber)
        Japanese: Saba Misoni (mackerel simmered in miso) with rice (Omega-3, Protein)
        Japanese: Shrimp Udon with bok choy and mushrooms (Omega-3, Protein)
        Japanese: Grilled Teriyaki chicken with sautéed vegetables (Protein, Fiber)
        Japanese: Yaki Tori (grilled chicken skewers) with rice (Protein, Fiber)
        Japanese: Unagi Don (grilled eel) with rice and vegetables (Omega-3, Protein)
        Japanese: Salmon Teriyaki with steamed rice and spinach (Omega-3, Protein)
        Japanese: Kakiage (vegetable fritters) with dipping sauce and rice (Fiber, Protein)
        Japanese: Beef Shogayaki (ginger stir-fried beef) with rice (Protein, Fiber)
        Japanese: Tofu Stir-fry with vegetables and miso sauce (Protein, Fiber)
    
    **30-39 years (Adults):**
        - Focus:
        The 30s often focus on maintaining a balanced lifestyle amidst career, family, and physical health management. The key focus is preventing health issues by making proactive choices for long-term well-being. There may also be changes in metabolism and muscle mass, which require adjustments in diet and physical activity.
        Stress management, healthy aging, and muscle preservation.
        Maintaining healthy body weight and metabolism, preventing midlife weight gain.
        Promoting mental clarity, reducing stress, and combating work-life imbalance.
        - Key Nutrients:
        Fiber: Helps manage weight, regulate blood sugar, and supports heart health.
        Protein: Vital for maintaining muscle mass and strength. This is particularly important as metabolism begins to slow in the 30s.
        Healthy Fats: Omega-3s, in particular, support brain health, inflammation reduction, and cardiovascular health.
        Antioxidants: Important for reducing oxidative stress and preventing early signs of aging, including skin and joint health.
        - Meal Suggestions:
        - **Breakfast:**
        Korean: Kimchi Pancakes (김치전) with a side of pickled vegetables (Protein, Fiber)
        Korean: Jeon (전) with zucchini, mushrooms, and egg (Protein, Fiber)
        Korean: Soondae (순대) - Korean blood sausage with vegetables (Protein, Iron)
        Korean: Mulhye (물회) - Cold raw fish soup with vegetables (Protein, Omega-3)
        Korean: Soft Boiled Egg with Gochujang and rice (Protein, Fiber)
        Western: Smoothie Bowl with spinach, berries, and chia seeds (Protein, Fiber)
        Western: Scrambled eggs with avocado and whole grain toast (Protein, Healthy Fats)
        Western: Almond butter and banana smoothie with almond milk (Protein, Fiber)
        Western: Whole grain oatmeal with flaxseed and mixed nuts (Fiber, Protein)
        Western: Protein smoothie with spinach, berries, and almond milk (Protein, Fiber)
        Western: Tofu and spinach scramble with avocado (Protein, Fiber)
        Western: Overnight oats with chia seeds, coconut milk, and mixed berries (Protein, Fiber)
        Western: Poached eggs on avocado toast with tomato (Protein, Healthy Fats)
        Western: Yogurt parfait with granola, chia seeds, and strawberries (Protein, Fiber)
        Western: Chia seed pudding with coconut milk, almonds, and strawberries (Protein, Fiber)
        Western: Spinach and mushroom frittata with quinoa (Protein, Fiber)
        Western: Protein pancakes with almond butter and blueberries (Protein, Fiber)
        Western: Greek yogurt with honey, walnuts, and mixed berries (Protein, Healthy Fats)
        Western: Whole wheat toast with almond butter, chia seeds, and banana slices (Protein, Fiber)
        Japanese: Miso soup with tofu, wakame seaweed, and green onions (Protein, Fiber)
        Japanese: Tamagoyaki (sweet Japanese omelet) with rice (Protein)
        Japanese: Japanese Pancakes (Okonomiyaki) with vegetables and pork (Protein, Fiber)
        Japanese: Chawanmushi (steamed egg custard) with shrimp and mushrooms (Protein, Fiber)
        Japanese: Teriyaki salmon with steamed rice and spinach (Omega-3, Protein)
        Japanese: Sushi rolls with tuna, avocado, and cucumber (Omega-3, Protein)
        Japanese: Katsu (breaded pork cutlet) with shredded cabbage (Protein, Fiber)
        Japanese: Edamame with a sprinkle of sea salt (Protein, Fiber)
        Japanese: Grilled mackerel with a side of miso soup (Omega-3, Protein)
        Japanese: Okonomiyaki (savory pancake) with pork belly and vegetables (Protein, Fiber)
        Japanese: Rice porridge (Okayu) with pickled vegetables (Fiber, Vitamins)
        - **Lunch:**
        Korean: Banchan (반찬) with grilled beef and vegetables (Protein, Fiber)
        Korean: Jjajangmyeon (짜장면) - Black bean paste noodles with pork (Protein, Fiber)
        Korean: Tofu Bibimbap (비빔밥) - Mixed rice with tofu and vegetables (Protein, Fiber)
        Korean: Gukbap (국밥) with pork and kimchi (Protein, Fiber)
        Korean: Oxtail Soup (꼬리곰탕) with steamed rice (Protein, Fiber)
        Western: Grilled chicken salad with mixed greens, tomatoes, and balsamic vinaigrette (Protein, Fiber)
        Western: Grilled pork chops with roasted sweet potatoes and broccoli (Protein, Fiber)
        Western: Grilled portobello mushrooms with quinoa and vegetables (Fiber, Protein)
        Western: Veggie burger with avocado and mixed greens (Protein, Fiber)
        Western: Quinoa-stuffed bell peppers with a side of mixed greens (Protein, Fiber)
        Western: Shrimp stir-fry with broccoli, carrots, and brown rice (Omega-3, Protein)
        Western: Chicken Caesar wrap with spinach (Protein, Fiber)
        Western: Grilled fish tacos with cabbage slaw and avocado (Omega-3, Protein)
        Western: Spaghetti with turkey meatballs and marinara sauce (Protein, Fiber)
        Western: Grilled shrimp with avocado and quinoa salad (Omega-3, Protein)
        Western: Grilled chicken breast with roasted potatoes and green beans (Protein, Fiber)
        Western: Quinoa bowl with roasted vegetables, chickpeas, and tahini dressing (Protein, Fiber)
        Western: Roasted chicken with mashed sweet potatoes and spinach (Protein, Fiber)
        Western: Baked salmon with roasted Brussels sprouts and quinoa (Omega-3, Protein)
        Japanese: Gyu Don (beef rice bowl) with vegetables (Protein, Fiber)
        Japanese: Tofu Katsu (breaded tofu cutlet) with rice (Protein, Fiber)
        Japanese: Teriyaki chicken with sautéed vegetables and rice (Protein, Fiber)
        Japanese: Soba noodles with tempura shrimp and vegetables (Omega-3, Protein)
        Japanese: Chicken karaage (fried chicken) with rice and miso soup (Protein, Fiber)
        Japanese: Tonkatsu (breaded pork) with steamed rice (Protein, Fiber)
        Japanese: Udon noodles with beef and onions (Protein, Fiber)
        Japanese: Grilled eel with rice and pickled vegetables (Omega-3, Protein)
        Japanese: Salmon Teriyaki with steamed vegetables and rice (Omega-3, Protein)
        Japanese: Salmon sashimi with rice and miso soup (Omega-3, Protein)
        Japanese: Sashimi platter with a variety of fish (Omega-3, Protein)
        - **Dinner:**
        Korean: Galbi (갈비) - Grilled beef short ribs with vegetables (Protein, Fiber)
        Korean: Kimchi Jjigae (김치찌개) - Kimchi stew with tofu and pork (Protein, Fiber)
        Korean: Samgyetang (삼계탕) - Ginseng chicken soup (Protein, Fiber)
        Korean: Tofu stew (두부찌개) with vegetables (Protein, Fiber)
        Korean: Pajeon (파전) - Korean savory pancake with green onions and seafood (Protein, Fiber)
        Western: Grilled chicken with roasted sweet potatoes and kale (Protein, Fiber)
        Western: Shrimp and vegetable stir-fry with brown rice (Omega-3, Protein)
        Western: Grilled steak with roasted potatoes and asparagus (Protein, Fiber)
        Western: Vegan chili with quinoa and avocado (Protein, Fiber)
        Western: Lemon herb grilled chicken with quinoa and steamed broccoli (Protein, Fiber)
        Western: Grilled chicken and vegetable kebabs with couscous (Protein, Fiber)
        Western: Baked cod with a side of quinoa and roasted vegetables (Protein, Fiber)
        Western: Grilled turkey breast with roasted Brussels sprouts and mashed potatoes (Protein, Fiber)
        Western: Baked salmon with quinoa and sautéed spinach (Omega-3, Protein)
        Western: Vegan lentil stew with mixed vegetables and quinoa (Fiber, Protein)
        Western: Baked chicken with roasted zucchini and sweet potatoes (Protein, Fiber)
        Western: Grilled shrimp with quinoa and roasted vegetables (Omega-3, Protein)
        Western: Vegan stuffed peppers with quinoa, beans, and avocado (Protein, Fiber)
        Western: Grilled lamb chops with quinoa and roasted vegetables (Protein, Fiber)
        Japanese: Shabu Shabu (hot pot) with tofu and vegetables (Protein, Fiber)
        Japanese: Unagi Don (grilled eel on rice) with pickled vegetables (Omega-3, Protein)
        Japanese: Tonkotsu Ramen (pork broth ramen) with vegetables (Protein, Fiber)
        Japanese: Chirashi Sushi (scattered sushi) with tuna and salmon (Omega-3, Protein)
        Japanese: Katsuobushi (dried bonito flakes) on rice with miso soup (Protein, Omega-3)
        Japanese: Yaki Tori (grilled chicken skewers) with steamed rice (Protein, Fiber)
        Japanese: Miso-glazed grilled mackerel with rice and spinach (Omega-3, Protein)
        Japanese: Gyoza (dumplings) with dipping sauce (Protein, Fiber)
        Japanese: Sukiyaki (beef hot pot) with tofu and vegetables (Protein, Fiber)
        Japanese: Grilled saba (mackerel) with rice and miso soup (Omega-3, Protein)
        Japanese: Vegetable tempura with rice (Fiber, Protein)
    **40-49 years (Adults):**
        - Focus:
        In the 40s, many experience changes in metabolism, muscle mass, and joint health. The key focus is to maintain a healthy weight, manage stress levels, and support healthy aging. Lifestyle choices become critical for preventing chronic conditions such as cardiovascular disease, diabetes, and joint degeneration.
        Maintaining bone density, joint health, and supporting metabolism to prevent weight gain.
        Preventing cardiovascular disease and managing cholesterol levels through healthy fats and antioxidants.
        Supporting cognitive health and mental well-being, with a focus on stress reduction.
        - Key Nutrients:
        Omega-3: Essential for reducing inflammation, supporting cardiovascular health, and improving brain function.
        Fiber: Helps reduce the risk of heart disease, manage blood sugar, and support digestive health.
        Calcium: Continues to play a significant role in bone health, helping to prevent osteoporosis.
        Protein: Important for maintaining lean muscle mass, which naturally declines with age.
        - Meal Suggestions:
        - **Breakfast:**
        Korean: Kimchi Bokkumbap (김치볶음밥) with a fried egg (Protein, Fiber)
        Korean: Juk (죽) - Rice porridge with abalone (Protein, Omega-3)
        Korean: Gyeranjjim (계란찜) - Steamed egg with vegetables (Protein, Fiber)
        Korean: Porridge with pumpkin and beans (Protein, Fiber)
        Korean: Steamed rice with grilled pork belly (Protein, Healthy Fats)
        Western: Quinoa porridge with almond butter and blueberries (Protein, Fiber)
        Western: Chia pudding with coconut milk, almonds, and mixed berries (Protein, Fiber)
        Western: Egg and avocado toast with cherry tomatoes (Protein, Healthy Fats)
        Western: Smoked salmon on whole grain toast with cucumber (Omega-3, Protein)
        Western: Scrambled eggs with spinach, tomatoes, and feta cheese (Protein, Fiber)
        Western: Green smoothie with kale, chia seeds, and almond milk (Protein, Fiber)
        Western: Whole wheat pancakes with almond butter and banana (Protein, Fiber)
        Western: Whole grain waffles with almond butter and chia seeds (Protein, Fiber)
        Western: Greek yogurt with chia seeds, honey, and granola (Protein, Fiber)
        Western: Protein-packed smoothie with peanut butter, banana, and almond milk (Protein, Healthy Fats)
        Western: Veggie-packed omelette with mushrooms, spinach, and tomatoes (Protein, Fiber)
        Western: Scrambled tofu with spinach and avocado (Protein, Fiber)
        Western: Overnight oats with chia seeds, almond milk, and strawberries (Protein, Fiber)
        Western: Breakfast burrito with eggs, spinach, and black beans (Protein, Fiber)
        Japanese: Tamago Sushi (sweet egg sushi) with cucumber (Protein, Fiber)
        Japanese: Chazuke (茶漬け) - Rice with green tea and salmon (Omega-3, Protein)
        Japanese: Nattō (fermented soybeans) with rice and pickles (Protein, Fiber)
        Japanese: Japanese yogurt with sweet red bean paste (Protein, Fiber)
        Japanese: Okonomiyaki (savory pancake) with shrimp and vegetables (Protein, Fiber)
        Japanese: Japanese rice ball (onigiri) with salmon filling (Omega-3, Protein)
        Japanese: Hiyayakko (冷やっこ) - Cold tofu with soy sauce and green onions (Protein, Fiber)
        Japanese: Shiso leaves with miso soup (Omega-3, Fiber)
        Japanese: Oyakodon (親子丼) - Chicken and egg rice bowl (Protein, Fiber)
        Japanese: Miso soup with salmon and vegetables (Omega-3, Protein)
        Japanese: Umeboshi (pickled plum) with steamed rice (Fiber, Vitamin C)
        - **Lunch:**
        Korean: Doenjang Chigae (된장찌개) with beef and tofu (Protein, Fiber)
        Korean: Kalbitang (갈비탕) - Beef short rib soup (Protein, Fiber)
        Korean: Dak Galbi (닭갈비) - Spicy stir-fried chicken with vegetables (Protein, Fiber)
        Korean: Bibim Naengmyeon (비빔냉면) - Cold spicy noodles with vegetables (Fiber, Protein)
        Korean: Samgyeopsal (삼겹살) - Grilled pork belly with kimchi (Protein, Healthy Fats)
        Western: Grilled turkey breast with quinoa salad and avocado (Protein, Fiber)
        Western: Grilled chicken Caesar salad with mixed greens (Protein, Fiber)
        Western: Veggie stir-fry with tofu and brown rice (Protein, Fiber)
        Western: Veggie and black bean taco with avocado and salsa (Protein, Fiber)
        Western: Baked chicken thighs with roasted carrots and quinoa (Protein, Fiber)
        Western: Grilled salmon with quinoa and mixed greens (Omega-3, Protein)
        Western: Grilled pork tenderloin with mashed sweet potatoes and green beans (Protein, Fiber)
        Western: Eggplant and quinoa casserole with mixed veggies (Fiber, Protein)
        Western: Grilled chicken sandwich with avocado and whole-grain bread (Protein, Healthy Fats)
        Western: Roasted vegetable and chickpea salad with tahini dressing (Fiber, Protein)
        Western: Roasted salmon with quinoa and sautéed kale (Omega-3, Protein)
        Western: Baked cod with roasted Brussels sprouts and quinoa (Protein, Fiber)
        Western: Spaghetti squash with marinara sauce and ground turkey (Protein, Fiber)
        Western: Grilled portobello mushrooms with couscous and roasted vegetables (Fiber, Protein)
        Japanese: Tonkatsu (breaded pork cutlet) with rice (Protein, Fiber)
        Japanese: Unagi Don (grilled eel with rice) and pickles (Omega-3, Protein)
        Japanese: Ramen with miso broth, tofu, and vegetables (Protein, Fiber)
        Japanese: Maki sushi with tuna and avocado (Omega-3, Protein)
        Japanese: Sukiyaki (beef hot pot) with tofu and vegetables (Protein, Fiber)
        Japanese: Teriyaki salmon with broccoli and quinoa (Omega-3, Protein)
        Japanese: Chirashi sushi (scattered sushi) with a variety of fish (Omega-3, Protein)
        Japanese: Tempura (fried vegetables) with rice (Protein, Fiber)
        Japanese: Grilled mackerel with miso soup and rice (Omega-3, Protein)
        Japanese: Udon noodles with seafood and spinach (Omega-3, Protein)
        Japanese: Bento box with grilled fish, rice, and vegetables (Omega-3, Fiber)
        - **Dinner:**
        Korean: Galbi Jjim (갈비찜) - Braised short ribs with vegetables (Protein, Fiber)
        Korean: Tofu Kimchi Jeongol (두부김치전골) - Stew with tofu and kimchi (Protein, Fiber)
        Korean: Kimchi Jeon (김치전) with rice (Protein, Fiber)
        Korean: Spicy Pork Stir-fry (제육볶음) with vegetables and rice (Protein, Fiber)
        Korean: Jangjorim (장조림) - Soy-braised beef with rice (Protein, Fiber)
        Western: Grilled lamb with quinoa and roasted vegetables (Protein, Fiber)
        Western: Grilled shrimp with garlic and quinoa (Omega-3, Protein)
        Western: Veggie lasagna with spinach and ricotta cheese (Protein, Fiber)
        Western: Roasted chicken with sweet potatoes and green beans (Protein, Fiber)
        Western: Grilled chicken skewers with roasted carrots and quinoa (Protein, Fiber)
        Western: Grilled steak with roasted potatoes and asparagus (Protein, Fiber)
        Western: Vegan chili with beans, quinoa, and avocado (Protein, Fiber)
        Western: Grilled turkey breast with roasted Brussels sprouts and mashed sweet potatoes (Protein, Fiber)
        Western: Roasted chicken with quinoa and steamed spinach (Protein, Fiber)
        Western: Baked salmon with roasted vegetables and quinoa (Omega-3, Protein)
        Western: Grilled fish tacos with cabbage and avocado (Omega-3, Protein)
        Western: Baked cod with quinoa and roasted Brussels sprouts (Protein, Fiber)
        Western: Grilled shrimp stir-fry with broccoli and rice (Omega-3, Protein)
        Western: Grilled chicken with roasted vegetables and quinoa (Protein, Fiber)
        Japanese: Yaki Udon (fried udon noodles) with vegetables and tofu (Protein, Fiber)
        Japanese: Saba Shioyaki (salt-grilled mackerel) with rice and miso soup (Omega-3, Protein)
        Japanese: Unagi Kabayaki (grilled eel) with rice and pickles (Omega-3, Protein)
        Japanese: Tonkotsu Ramen with pork and vegetables (Protein, Fiber)
        Japanese: Gyu Don (beef rice bowl) with vegetables (Protein, Fiber)
        Japanese: Grilled fish (mackerel) with miso soup and rice (Omega-3, Protein)
        Japanese: Bento box with rice, fish, and pickled vegetables (Omega-3, Fiber)
        Japanese: Okonomiyaki (savory pancake) with seafood (Protein, Fiber)
        Japanese: Teriyaki chicken with rice and sautéed vegetables (Protein, Fiber)
        Japanese: Tempura Udon with shrimp and vegetables (Protein, Fiber)
        Japanese: Chanko Nabe (sumo stew) with tofu and vegetables (Protein, Fiber)
    **50-59 years (Adults):**
        - Focus:
        In the 50s, the focus shifts toward maintaining overall health and preventing chronic diseases. Many individuals in this age group experience changes in metabolism, joint health, and energy levels. The goal is to maintain vitality, heart health, and optimal weight while managing symptoms of aging and stress.
        Supporting cardiovascular health, including managing cholesterol and blood pressure.
        Maintaining muscle strength, bone density, and joint health to remain physically active.
        Managing stress and ensuring mental clarity, which can be impacted by the aging process.
        - Key Nutrients:
        Omega-3: Supports heart health, reduces inflammation, and maintains cognitive function.
        Calcium: Key for bone strength and preventing osteoporosis, especially for post-menopausal women.
        Fiber: Crucial for maintaining digestive health, controlling blood sugar, and preventing heart disease.
        Protein: Helps to prevent muscle loss, supports healthy metabolism, and maintains overall physical strength.
        - Meal Suggestions:
        - **Breakfast:**
        Korean: Kimchi Jeon (김치전) with a boiled egg (Protein, Fiber)
        Korean: Gyeran Jjim (계란찜) with spinach and tofu (Protein, Calcium)
        Korean: Doenjang Jjigae (된장찌개) with mushrooms (Fiber, Protein)
        Korean: Oi Naengguk (오이냉국) with pickled cucumber and tofu (Fiber, Probiotics)
        Korean: Banchan (반찬) with grilled fish and rice (Omega-3, Protein)
        Western: Whole grain pancakes with almond butter and blueberries (Fiber, Healthy fats)
        Western: Quinoa and chia pudding with almond milk and honey (Fiber, Omega-3)
        Western: Scrambled eggs with avocado and mixed greens (Protein, Healthy fats)
        Western: Steel-cut oatmeal with flaxseeds, chia seeds, and almonds (Fiber, Omega-3)
        Western: Greek yogurt with walnuts and honey (Protein, Calcium)
        Western: Avocado smoothie with kale and chia seeds (Healthy fats, Fiber)
        Western: Baked eggs with spinach, mushrooms, and cheese (Protein, Calcium)
        Japanese: Tamago (Egg) sushi with rice (Protein, Fiber)
        Japanese: Miso soup with tofu and seaweed (Protein, Fiber, Calcium)
        Japanese: Onigiri (rice ball) with tuna and avocado (Omega-3, Protein)
        Japanese: Natto (fermented soybeans) with rice (Protein, Fiber, Probiotics)
        Japanese: Rice porridge (Okayu) with pickled vegetables (Fiber, Vitamins)
        Western: Smoothie bowl with berries, granola, and chia seeds (Fiber, Antioxidants)
        Western: Almond butter on whole-grain toast with banana (Healthy fats, Fiber)
        Western: Chia and flaxseed pudding with almond milk (Omega-3, Fiber)
        Western: Poached egg with avocado and tomato on whole-grain toast (Protein, Healthy fats)
        Western: Green smoothie with spinach, banana, and coconut milk (Fiber, Antioxidants)
        Korean: Tofu stew with vegetables and kimchi (Protein, Fiber)
        Korean: Juk (죽) with ginseng and mushrooms (Fiber, Antioxidants)
        Korean: Jeonbokjuk (전복죽) with abalone (Protein, Omega-3)
        Western: Cottage cheese with strawberries and walnuts (Protein, Calcium)
        Western: Baked quinoa and egg muffins with spinach (Fiber, Protein)
        Western: Protein smoothie with almond milk, spinach, and chia (Protein, Omega-3)
        Western: Whole-grain toast with poached egg, avocado, and tomato (Protein, Healthy fats)
        Western: Oatmeal with nuts, honey, and coconut flakes (Fiber, Healthy fats)
        - **Lunch:**
        Korean: Bulgogi (불고기) with quinoa and grilled vegetables (Protein, Fiber)
        Korean: Kimchi Jjigae (김치찌개) with tofu and rice (Probiotics, Protein)
        Korean: Samgyeopsal (삼겹살) with steamed broccoli (Protein, Healthy fats)
        Korean: Jajangmyeon (짜장면) with pork and vegetables (Protein, Fiber)
        Korean: Sundubu Jjigae (순두부찌개) with vegetables and tofu (Protein, Fiber)
        Western: Grilled chicken salad with kale, avocado, and walnuts (Protein, Healthy fats)
        Western: Grilled turkey and quinoa bowl with roasted vegetables (Protein, Fiber)
        Western: Roasted vegetable and chickpea salad with tahini dressing (Fiber, Protein)
        Western: Tuna salad with mixed greens, avocado, and olive oil (Omega-3, Protein)
        Western: Grilled salmon with quinoa and steamed vegetables (Omega-3, Protein)
        Western: Vegetable stir-fry with tofu and brown rice (Protein, Fiber)
        Western: Grilled vegetable wrap with hummus and falafel (Fiber, Protein)
        Japanese: Teriyaki salmon with steamed vegetables and rice (Omega-3, Protein)
        Japanese: Sashimi platter with tuna, salmon, and avocado (Omega-3, Protein)
        Japanese: Udon noodles with tofu and spinach (Protein, Fiber)
        Japanese: Tonkatsu (breaded pork) with steamed vegetables (Protein, Fiber)
        Western: Veggie burger with whole-grain bun and avocado (Fiber, Protein)
        Western: Sweet potato and black bean salad with quinoa (Fiber, Protein)
        Western: Grilled shrimp salad with avocado and cucumber (Omega-3, Protein)
        Western: Grilled chicken with roasted potatoes and green beans (Protein, Fiber)
        Korean: Grilled mackerel with steamed rice and vegetables (Omega-3, Protein)
        Korean: Grilled tofu with kimchi and quinoa (Protein, Fiber)
        Western: Chicken Caesar salad with kale (Protein, Healthy fats)
        Western: Baked falafel with hummus and tabbouleh (Protein, Fiber)
        Western: Baked salmon with roasted sweet potatoes (Omega-3, Protein)
        Western: Roasted turkey breast with quinoa and Brussels sprouts (Protein, Fiber)
        Japanese: Miso soup with tofu, seaweed, and vegetables (Protein, Fiber)
        Japanese: Grilled eel (Unagi) with rice (Omega-3, Protein)
        Korean: Bibimbap (비빔밥) with tofu and vegetables (Protein, Fiber)
        Western: Baked chicken breast with spinach and quinoa (Protein, Fiber)
        - **Dinner:**
        Korean: Galbitang (갈비탕) with rice (Protein, Calcium, Iron)
        Korean: Kimchi Bokkeumbap (김치볶음밥) with tofu and vegetables (Fiber, Protein)
        Korean: Tofu stir-fry with mushrooms and rice (Protein, Fiber)
        Korean: Doenjang Jjigae (된장찌개) with tofu and steamed vegetables (Protein, Fiber)
        Korean: Dak Galbi (닭갈비) with grilled vegetables (Protein, Fiber)
        Western: Grilled chicken breast with quinoa and steamed broccoli (Protein, Fiber)
        Western: Baked fish with mashed cauliflower and green beans (Omega-3, Protein)
        Western: Grilled lamb chops with quinoa and asparagus (Protein, Fiber)
        Western: Spaghetti with marinara sauce and turkey meatballs (Protein, Fiber)
        Western: Quinoa-stuffed bell peppers with grilled chicken (Fiber, Protein)
        Western: Baked salmon with roasted sweet potatoes (Omega-3, Protein)
        Western: Sweet potato fries with grilled turkey (Fiber, Protein)
        Western: Grilled shrimp with mixed greens and avocado (Omega-3, Protein)
        Western: Vegetable stir-fry with tofu and quinoa (Protein, Fiber)
        Western: Turkey meatloaf with roasted vegetables (Protein, Fiber)
        Japanese: Beef Sukiyaki (すき焼き) with tofu and vegetables (Protein, Fiber)
        Japanese: Grilled mackerel with steamed rice and vegetables (Omega-3, Protein)
        Japanese: Teriyaki chicken with quinoa and vegetables (Protein, Fiber)
        Korean: Banchan (반찬) with grilled fish and steamed vegetables (Omega-3, Protein)
        Korean: Grilled tofu with kimchi and quinoa (Protein, Fiber)
        Western: Grilled steak with roasted sweet potatoes and spinach (Protein, Fiber)
        Western: Spaghetti squash with marinara sauce and turkey (Protein, Fiber)
        Western: Chicken stir-fry with vegetables and brown rice (Protein, Fiber)
        Western: Grilled salmon with roasted Brussels sprouts (Omega-3, Protein)
        Korean: Grilled mackerel with kimchi and rice (Omega-3, Protein)
        Korean: Sundubu Jjigae (순두부찌개) with vegetables (Protein, Fiber)
        Japanese: Udon noodles with tofu and vegetables (Protein, Fiber)
        Japanese: Tonkotsu ramen with pork and vegetables (Protein, Fiber)
        Western: Baked chicken breast with spinach and quinoa (Protein, Fiber)
        Western: Shrimp stir-fry with quinoa and broccoli (Omega-3, Protein)
    
    **60+ years (Seniors):**
        - Focus:
        In the senior years, maintaining independence and quality of life becomes a priority. Focus is on preventing and managing chronic diseases, maintaining bone and joint health, and improving digestion. Nutrient-dense foods are crucial to ensure that the body continues to receive adequate nutrients for daily function and health maintenance.
        Maintaining muscle mass and functional strength to reduce the risk of falls and fractures.
        Supporting digestive health to counteract slower digestion and nutrient absorption.
        Focus on heart health and blood circulation to manage age-related conditions such as hypertension.
        - Key Nutrients:
        Calcium: Important for maintaining bone density and preventing fractures, especially in postmenopausal women and older men.
        Fiber: Helps manage constipation, lower cholesterol, and regulate blood sugar, which can be more challenging in older age.
        Omega-3: Reduces inflammation, supports cognitive health, and promotes cardiovascular well-being.
        Protein: Essential for maintaining muscle mass and strength, preventing sarcopenia, and supporting recovery from illness or surgery.
        - Meal Suggestions:
        - **Breakfast:**
        Korean: Tofu and vegetable stew (두부채소찌개) with rice (Protein, Calcium)
        Korean: Galbitang (갈비탕) with steamed vegetables (Protein, Calcium)
        Korean: Kimchi Jeon (김치전) with eggs (Protein, Fiber)
        Korean: Tofu and spinach stew (두부시금치국) with a side of rice (Protein, Fiber)
        Korean: Seaweed soup (미역국) with tofu and rice (Calcium, Protein)
        Western: Greek yogurt with chia seeds, flaxseeds, and walnuts (Protein, Omega-3)
        Western: Oatmeal with chia seeds, berries, and almond butter (Fiber, Omega-3)
        Western: Whole-grain toast with scrambled eggs, avocado, and spinach (Protein, Healthy fats)
        Western: Almond milk smoothie with spinach, banana, and chia seeds (Fiber, Calcium)
        Western: Scrambled eggs with tomatoes and mushrooms on whole-grain toast (Protein, Fiber)
        Western: Cottage cheese with strawberries, walnuts, and flaxseeds (Protein, Omega-3)
        Western: Overnight oats with almond milk, chia seeds, and berries (Fiber, Omega-3)
        Japanese: Miso soup with tofu and seaweed (Protein, Fiber)
        Japanese: Tamagoyaki (Japanese rolled omelet) with rice (Protein, Calcium)
        Japanese: Rice porridge (Okayu) with pickled vegetables (Fiber, Probiotics)
        Japanese: Rice and natto (fermented soybeans) (Protein, Probiotics)
        Japanese: Grilled fish (such as mackerel) with rice and miso soup (Omega-3, Protein)
        Western: Chia pudding with almond milk and mixed berries (Fiber, Omega-3)
        Western: Smoothie bowl with berries, almond butter, and granola (Fiber, Protein)
        Western: Avocado toast with poached eggs and arugula (Healthy fats, Protein)
        Western: Poached eggs with spinach and mushrooms (Protein, Calcium)
        Western: Green smoothie with kale, cucumber, and lemon (Fiber, Antioxidants)
        Korean: Kimchi with steamed tofu (Probiotics, Protein)
        Korean: Oatmeal with soy milk, walnuts, and chia seeds (Fiber, Omega-3)
        Western: Protein smoothie with almond milk, spinach, and chia seeds (Protein, Omega-3)
        Western: Quinoa and chia pudding with almond milk and honey (Fiber, Omega-3)
        Western: Scrambled eggs with smoked salmon and spinach (Omega-3, Protein)
        Western: Whole grain pancakes with blueberries and honey (Fiber, Antioxidants)
        Western: Oatmeal with flaxseeds, chia seeds, and almond butter (Fiber, Omega-3)
        Western: Greek yogurt parfait with granola, walnuts, and berries (Protein, Omega-3)
        - **Lunch:**
        Korean: Bulgogi (불고기) with steamed rice and vegetables (Protein, Fiber)
        Korean: Doenjang Jjigae (된장찌개) with tofu and mushrooms (Protein, Fiber)
        Korean: Grilled fish (mackerel) with steamed broccoli and rice (Omega-3, Protein)
        Korean: Samgyeopsal (삼겹살) with kimchi and grilled vegetables (Protein, Fiber)
        Korean: Chicken Bibimbap (비빔밥) with assorted vegetables (Protein, Fiber)
        Western: Grilled chicken salad with avocado, spinach, and walnuts (Protein, Healthy fats)
        Western: Grilled salmon with quinoa and steamed vegetables (Omega-3, Protein)
        Western: Turkey wrap with avocado, lettuce, and tomatoes (Protein, Healthy fats)
        Western: Roasted vegetable quinoa salad with chickpeas (Fiber, Protein)
        Western: Veggie burger with avocado and spinach on whole-grain bun (Protein, Fiber)
        Western: Grilled shrimp with mixed greens and avocado (Omega-3, Protein)
        Western: Grilled chicken with roasted sweet potatoes and kale (Protein, Fiber)
        Japanese: Teriyaki salmon with sautéed spinach and rice (Omega-3, Protein)
        Japanese: Sushi rolls with avocado and cucumber (Omega-3, Fiber)
        Japanese: Tofu stir-fry with broccoli and bell peppers (Protein, Fiber)
        Japanese: Grilled eel (Unagi) with rice (Omega-3, Protein)
        Japanese: Sashimi (tuna, salmon) with miso soup (Omega-3, Protein)
        Western: Spinach and feta stuffed chicken breast with quinoa (Protein, Fiber)
        Western: Sweet potato and black bean salad with quinoa (Fiber, Protein)
        Western: Grilled turkey burger with a side of mixed greens (Protein, Fiber)
        Western: Baked cod with roasted cauliflower and quinoa (Protein, Fiber)
        Western: Roasted vegetable and chickpea bowl with tahini dressing (Fiber, Protein)
        Korean: Grilled mackerel with quinoa and kimchi (Omega-3, Protein)
        Korean: Galbi (갈비) with grilled vegetables (Protein, Calcium)
        Korean: Spicy tofu stew with spinach and mushrooms (Protein, Fiber)
        Western: Baked chicken with roasted sweet potatoes and asparagus (Protein, Fiber)
        Western: Quinoa-stuffed bell peppers with grilled shrimp (Fiber, Omega-3)
        Western: Grilled chicken with avocado and quinoa salad (Protein, Healthy fats)
        Western: Grilled salmon with lemon butter and steamed spinach (Omega-3, Protein)
        Western: Mediterranean chicken bowl with hummus and vegetables (Protein, Fiber)
        - **Dinner:**
        Korean: Dak Jjim (닭찜) with sweet potatoes and steamed vegetables (Protein, Fiber)
        Korean: Banchan (반찬) with grilled fish and rice (Omega-3, Protein)
        Korean: Doenjang Jjigae (된장찌개) with tofu and vegetables (Protein, Fiber)
        Korean: Grilled mackerel with steamed rice and spinach (Omega-3, Protein)
        Korean: Grilled tofu with kimchi and steamed broccoli (Protein, Fiber)
        Western: Grilled lamb chops with quinoa and green beans (Protein, Fiber)
        Western: Baked salmon with roasted cauliflower and quinoa (Omega-3, Protein)
        Western: Grilled chicken breast with roasted potatoes and mixed greens (Protein, Fiber)
        Western: Spaghetti with marinara sauce and turkey meatballs (Protein, Fiber)
        Western: Quinoa-stuffed bell peppers with grilled chicken (Fiber, Protein)
        Western: Grilled shrimp stir-fry with quinoa and mixed vegetables (Omega-3, Protein)
        Western: Baked cod with roasted Brussels sprouts and quinoa (Protein, Fiber)
        Western: Grilled turkey burger with a side of sweet potato fries (Protein, Fiber)
        Western: Grilled steak with roasted vegetables and quinoa (Protein, Fiber)
        Japanese: Beef Sukiyaki (すき焼き) with tofu and vegetables (Protein, Fiber)
        Japanese: Grilled fish (mackerel) with miso soup (Omega-3, Protein)
        Japanese: Teriyaki chicken with quinoa and roasted vegetables (Protein, Fiber)
        Japanese: Udon noodles with tofu and spinach (Protein, Fiber)
        Japanese: Tonkatsu (breaded pork) with steamed broccoli (Protein, Fiber)
        Western: Baked chicken with roasted sweet potatoes and green beans (Protein, Fiber)
        Western: Grilled steak with quinoa and roasted vegetables (Protein, Fiber)
        Western: Baked turkey breast with Brussels sprouts (Protein, Fiber)
        Western: Grilled shrimp with garlic and quinoa (Omega-3, Protein)
        Western: Grilled chicken with quinoa and steamed broccoli (Protein, Fiber)
        Western: Sweet potato and kale salad with chickpeas and quinoa (Fiber, Protein)
        Korean: Kimchi Jjigae (김치찌개) with tofu and rice (Probiotics, Protein)
        Korean: Grilled fish with steamed rice and kimchi (Omega-3, Protein)
        Korean: Jajangmyeon (짜장면) with pork and vegetables (Protein, Fiber)
        Korean: Samgyetang (삼계탕) with ginseng and chicken (Protein, Fiber)
        Korean: Grilled tofu with mushrooms and vegetables (Protein, Fiber)
        
    - **Diet Status Adjustments:**
        - Determining Diet Status: The user's diet status can be identified using the variable {is_on_diet}, which can have two possible values:
        - **On a diet:** The user is focused on maintaining a specific weight goal or following a health regimen such as calorie reduction, fat loss, or muscle gain.
            - On a Diet: If the user is on a diet, the primary goal is typically weight loss, muscle definition, or improved metabolic health. For these purposes, the meal recommendations should prioritize:
            - Low-calorie, high-protein meals to support muscle repair, minimize fat storage, and keep the user feeling satiated longer.
            - High-fiber foods that aid in digestion, improve gut health, and contribute to feelings of fullness, thus preventing overeating.
            - Healthy fats like those found in avocados, nuts, and seeds to support hormone production and satiety.
            Recommended Meal Characteristics:=
            - Protein: Protein is essential for muscle repair and growth. Meals should contain lean sources of protein such as chicken breast, fish (especially fatty fish like salmon for omega-3s), eggs, or plant-based proteins like tofu and legumes. The goal is 20-30 grams of protein per meal.
            - Fiber: Fiber-rich foods such as vegetables, whole grains (like quinoa or brown rice), and legumes (lentils, chickpeas) help improve digestion, regulate blood sugar, and keep you full between meals. Aim for 5-10 grams of fiber per meal.
            - Healthy Fats: Healthy fats are crucial for maintaining metabolic rate and ensuring nutrient absorption. Foods like avocado, olive oil, nuts, and seeds should be incorporated in moderation, aiming for about 10-15 grams of fat per meal.
            - Low Glycemic Index: Avoid foods with a high glycemic index (e.g., white bread, sugary snacks), as they can lead to blood sugar spikes and crashes. Instead, focus on complex carbohydrates that release energy slowly.
            - Portion Control: Since the goal is weight loss or maintenance, portion control is vital. Meals should be filling but lower in calorie density, so that the user can enjoy a satisfying portion without overconsuming calories.
        - **Not on a diet:** The user is not specifically restricting calories or following any formal dietary regimen. They may focus on a balanced, healthy approach to eating, with diverse ingredients and overall well-being in mind.
            - Not on a Diet:
            - If the user is not on a diet, the focus should shift to providing a well-rounded, balanced diet that supports overall health and well-being, rather than weight loss or muscle gain. The goal here is to ensure the body receives a variety of nutrients, while still promoting optimal health.
            Recommended Meal Characteristics:
            - Balanced Macronutrients: Meals should include a healthy balance of protein, carbohydrates, and fats. This will support energy levels, muscle maintenance, and overall bodily function.
            - Micronutrient-Rich Foods: Emphasize a wide variety of fruits, vegetables, and whole grains to ensure the intake of essential vitamins and minerals. Consider the inclusion of leafy greens (e.g., kale, spinach), cruciferous vegetables (e.g., broccoli, cauliflower), and fruits high in antioxidants (e.g., berries, citrus fruits).
            - Moderate Portions: While portion control may not be as strict as for those on a diet, it is still important to eat in moderation. The focus should be on wholesome, nutrient-dense foods, with fewer processed options.
            - Carbohydrates for Energy: Complex carbohydrates such as whole grains, starchy vegetables, and legumes should make up a substantial portion of the meal. These provide steady energy release and support physical activity throughout the day.
            - Inclusion of Healthy Fats: Moderate amounts of healthy fats, such as those from nuts, seeds, olive oil, and fatty fish, are important for brain function and cell health.
        - Additional Notes:
            Hydration:
            Both for individuals on a diet and not, staying hydrated is crucial. Water plays an essential role in digestion, nutrient absorption, and energy levels. Consider recommending herbal teas or water-rich fruits (like cucumbers or watermelon) throughout the day.
            Meal Timing:
            For those on a diet, focusing on meal frequency may be helpful. Some individuals prefer eating smaller meals throughout the day to manage hunger and blood sugar levels. On the other hand, those not on a diet may find it beneficial to focus on 3 larger, balanced meals with snacks in between.
            Lifestyle Factors:
            Additional factors like exercise, sleep quality, and stress management can significantly influence the effectiveness of diet plans. For users who are active, a higher protein intake is beneficial for muscle repair. For those with high-stress levels, foods rich in magnesium (like spinach, nuts, and seeds) and omega-3s (from fatty fish) are helpful for reducing stress hormones.
    - **Example Recommendations:**
        - Describe the nutrient composition (protein, fat, carbohydrates) and health benefits (muscle recovery, blood sugar control, heart health) of each meal.
        - Explain how each ingredient helps the user achieve their dietary goals.

    ### **Example Meal Recommendation Adjustments:**
    - If the user had a calorie-dense meal for breakfast (e.g., 김치 찌개), suggest lighter, nutrient-dense options like a vegetable-based salad or a protein-packed meal like grilled chicken for lunch or dinner. Emphasize the need to balance calories and nutrients.
    - If the user has already consumed foods rich in fat or sugar, advise on foods with higher fiber or protein to balance out the nutrient profile for the rest of the day.

    ### **Output Format** -> must be cleared on each menu
    - Ensure that every response includes the following:
    1. **Meal Name**
    2. **Nutritional Composition (calories, protein, fats, carbohydrates, and key micronutrients)**
    3. **Why Recommended at this Time (based on previous meals)**
    4. **Health Benefits**

    Example of whole format: 
    ### If the user ate the meal at dinner, considering what user ate for breakfast({breakfast_time}) and lunch({launch_time}), you must recommend for next morning menu
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
    비타민/미네랄: 신선한 채소와 과일로 보충 필요
    
    ### 5. 내일 아침 식사 추천***please consider the variety of food***
    - **메뉴**: 오트밀, 삶은 계란, 아보카도, 과일 (사과, 블루베리)
    오트밀: 
    삶은 계란: 복합 탄수화물을 제공하여 혈당을 천천히 안정시킵니다. 오트밀은 섬유질이 풍부하여 소화기 건강을 돕고, 장내 유익균 증식을 지원합니다. 또한 철분과 마그네슘, 비타민 B군이 함유되어 에너지 생산과 신경 건강에 기여합니다.
    건강 효과: 혈당 조절에 도움을 주고, 심혈관 건강을 개선하는 데 효과적입니다. 지속적인 에너지원으로 아침에 피로를 덜어주고, 장 건강을 개선할 수 있습니다.
    
    아보카도: 고품질 단백질을 제공하며, 비타민 B군(특히 B12와 엽산)과 비타민 D가 풍부합니다. 계란에 포함된 콜린은 뇌 기능과 신경 건강에 중요한 역할을 하며, 아미노산이 근육 회복과 유지에 필수적입니다.
    건강 효과: 근육 유지와 회복에 도움을 주며, 면역력 강화와 신경 건강 개선에 기여합니다. 계란은 포만감을 유지시켜 체중 관리에도 유리합니다.

    과일 (사과, 블루베리):
    사과는 섬유질이 풍부하여 소화를 돕고, 비타민 C와 항산화 물질이 피부와 면역력 강화에 도움을 줍니다.
    블루베리는 항산화 물질(특히 플라보노이드)이 풍부하여 세포 보호, 노화 방지 및 면역력 증진에 중요한 역할을 합니다. 비타민 C와 식이섬유도 풍부하여 장 건강을 개선합니다.
    건강 효과: 항산화 물질이 세포를 보호하고, 면역력 강화를 돕습니다. 피부 건강을 증진시키며, 체내 염증을 줄여주는 효과가 있습니다.
    
    ### 7. 건강 이점:
    오트밀: 천천히 소화되며 혈당을 안정적으로 유지합니다. 섬유질이 풍부하여 소화를 돕고, 장 건강을 개선합니다. 또한 심혈관 질환 예방에 도움을 주며, 체중 관리에 효과적입니다.
    삶은 계란: 고품질 단백질과 필수 아미노산을 제공하여 근육 회복에 도움을 줍니다. 또한 비타민 B군과 콜린이 뇌 기능을 지원하며, 체내 에너지 생산에 필수적입니다.
    아보카도: 불포화지방과 칼륨이 풍부하여 심혈관 건강을 개선하고, 피부와 뇌 건강을 지원합니다. 항염증 작용을 통해 체내 염증을 줄이며, 체중 관리에 도움이 됩니다.
    과일 (사과, 블루베리): 비타민 C와 항산화 물질이 풍부하여 면역력 강화를 돕고, 피부 건강을 증진시키며, 세포 노화를 방지합니다.
    이렇게 아침으로 김치 찌개를 드셨으므로, 점심과 저녁은 단백질과 미세 영양소를 충분히 보충하여 균형 잡힌 식사를 유지할 수 있게 도와드립니다.
    ***Always adjust recommendations based on what the user has already consumed in their meals. Provide context-sensitive meal plans that ensure nutrient balance and support the user's dietary goals.***
    """},
    {'role': 'user', 'content': chosen_language},
    {'role': 'user', 'content': response},
    {'role': 'user', 'content': time},
    {'role': 'user', 'content': food_time},
    {'role': 'user', 'content': breakfast_time},
    {'role': 'user', 'content': launch_time},
    {'role': 'user', 'content': age},
    {'role': 'user', 'content': is_on_diet},
    ], stream=True)
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True) 
            output += content

#return한 ouput을 받아 지속적인 질문을 받는 함수
def questions(output):
    global question
    continue_question = input('\n혹시 질문이나 궁금하신 점 있을까요? ')
    client = OpenAI()
    completion = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': """
            You are a master chef and a helpful health trainer. You will receive multiple questions based on {output} but don't make any duplicated answers.
            1. **Answer the Question**
            - Provide a thorough and informative response to each question.
            2. **Detailed Instructions**
            - If the user asks how to make specific ***ingredients***, provide a detailed, step-by-step explanation on how to prepare them.
            3. **chat history**
            - If user is asking a question regarding previous chat, try to find it in {recommendation_history}
            **Notes:**
            - Ensure all responses are clear, concise, and relevant to the user's queries.
            - Maintain a professional and friendly tone throughout the conversation.
            """},
            {'role': 'user', 'content': output},
            {'role': 'user', 'content': continue_question},
        ], stream= True)
    question_output = []
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True) 
            question += content
    return question_output

dinner_calculator() #추후의 변경
