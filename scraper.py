import requests
import bs4 as BeautifulSoup
#product_code = input("Please enter product code")
product_code = "129901214"

url= f"https://www.ceneo.pl/{product_code}#tab=reviews"
response = requests.get(url)
if response.status_code == requests.codes.ok:
    page_dom = BeautifulSoup(response.text, "html.parser")
    opinions = page_dom.select("div.js_product-review")
    if len(opinions)>0:
        all_opinions = []
        print(f"There are some opinions about product with {product_code}code.")
        for opinion in opinions:
            opinion_id = opinion["data-entry-id"]
            author = opinion.select_one("span.user-post__author-name").text.strip()
            single_opinion = {
                "opinion_id": opinion_id,
                "author": author,
                "authors recommendation": recommendation,
                "score" : score,
                "description" : description,
                "pros": pros,
                "cons":cons,
                "like": like,
                "dislike": dislike,
                "publish_date": publish_date,
                "purchase_date": purchase_date

            }
            all_opinions.append(single_opinion)
        url = "https://ceneo.pl" + page_dom.select_one("a.pagination_next")["href"]
        print(url)
    else:    
         print(f"There are no opinions about product with {product_code}code.")
open(f"./opinions/{product_code}.json", "w", encodimg="UTF-8") as jf:
json.dump(all_opinions.jf, imdent=4,ensure_ascii=False)
