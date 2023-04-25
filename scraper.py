import json
import requests
from bs4 import BeautifulSoup

def get_element(dom_tree, selector = None, attribute = None):
    try:
        if attribute:
            if selector:
                return dom_tree[attribute]
            return dom_tree.select_one(selector).text.strip
    except AttributeError:
        return None

product_code = input("Please enter the product code: ")
# product_code = "129910940"
# print(product_code)
# product_code = "150607728"

url = f"https://www.ceneo.pl/{product_code}#tab=reviews"
all_opinions = []
while url:
    
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        page_dom = BeautifulSoup(response.text, "html.parser")
        print(get_element(page_dom))
        opinions = page_dom.select("div.js_product-review")
        if len(opinions)>0:
            
            print(f"There are some opinions about product with {product_code} code.")
            for opinion in opinions:
                opinion_id = opinion["data-entry-id"]
                author = get_element(opinion.select_one("span.user-post__author-name").text.strip())
                try:
                    recommendation = opinion.select_one("span.user-post__author-recomendation > em").text.strip()
                except AttributeError:
                    recommendation = None
                score = get_element(opinion.select_one("span.user-post__score-count").text.strip())
                description = get_element(opinion.select_one("div.user-post__text").text.strip())
                pros = get_element(opinion.select("div.review-feature__col:has( > div.review-feature__title--positives)> div.review-feature__item"))
                pros = [p.text.strip() for p in pros]
                cons = opinion.select("div.review-feature__col:has( > div.review-feature__title--negatives)> div.review-feature__item")
                cons = [c.text.strip() for c in cons]
                like = get_element(opinion.select_one("button.vote-yes")["data-total-vote"].strip())
                dislike = get_element(opinion.select_one("button.vote-no")["data-total-vote"].strip())
                publish_date = get_element(opinion.select_one("span.user-post__published > time:nth-child(1)","datetime"))
                
                single_opinion = {
                    "opinion-id": opinion_id,
                    "author": author,
                    "authors recommendation": recommendation,
                    "score": score,
                    "description": description,
                    "pros": pros,
                    "cons": cons,
                    "like": like,
                    "dislike": dislike,
                    "publishing date": publish_date,
                    "purschase date": purchase_date
                }
                all_opinions.append(single_opinion)
            try:
                url = "https://www.ceneo.pl" + page_dom.select_one("a.pagination__next")["href"]
            except TypeError:
                url = None
            print(url)
            
        else:
            print(f"There are no opinions about product with {product_code} code.")
            url = None
    print(url)
if len(all_opinions) > 0:
    with open(f"./opinions/{product_code}.json", "w", encoding="UTF-8") as jf:
        json.dump(all_opinions, jf, indent=4, ensure_ascii=False)