import requests
import bs4
import pandas as pd # type: ignore

url = 'https://m.10000recipe.com/recipe/list.html'

final_data = []

for i in range(1, 6):
    new_url = f'{url}?page={i}'
    res = requests.get(new_url)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    items = soup.find_all("div", "media")

    for item in items:
        title = item.find("span", "jq_elips2").text.strip()
        author = item.find("div", "info_name").text.strip()
        try:
            image = item.find("img", "media-object")["src"]
        except Exception as e:
            image = ""
            print(e)
        
        final_data.append({
            "title": title,
            "author": author,
            "image": image
        })

df = pd.DataFrame(final_data)
df.to_csv("result.csv")