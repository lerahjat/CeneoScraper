import os
import json
import requests
import numpy as np
from bs4 import BeautifulSoup
from translate import Translator

def get_element(dom_tree, selector = None, attribute = None, return_list = False):
    try:
        if return_list:
            return ", ".join([tag.text.strip() for tag in dom_tree.select(selector)])
        if attribute:
            if selector:
                return dom_tree.select_one(selector)[attribute].strip()
            return dom_tree[attribute]
        return dom_tree.select_one(selector).text.strip()
    except (AttributeError,TypeError):
        return None

def clean_text(text):
    return ' '.join(text.replace(r"\s", " ").split())

selectors = {
    "opinion_id": [None, "data-entry-id"],
    "author": ["span.user-post__author-name"],
    "recommendation": ["span.user-post__author-recomendation > em"],
    "score": ["span.user-post__score-count"],
    "description": ["div.user-post__text"],
    "pros": ["div.review-feature__col:has( > div.review-feature__title--positives) > div.review-feature__item", None, True],
    "cons": ["div.review-feature__col:has( > div.review-feature__title--negatives) > div.review-feature__item", None, True],
    "like": ["button.vote-yes > span"],
    "dislike": ["button.vote-no > span"],
    "publish_date": ["span.user-post__published > time:nth-child(1)","datetime"],
    "purchase_date": ["span.user-post__published > time:nth-child(2)","datetime"]
}

from_lang = "pl"
to_lang = "en"
translator = Translator(to_lang, from_lang)

product_code = input("Please enter product code: ")
# product_code = "129901214"
# product_code = "150607728"
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}
url = f"https://www.ceneo.pl/{product_code}#tab=reviews"
all_opinions = []
while url:
    print(url)
    response = requests.get(url, headers=headers)
    if  response.status_code == requests.codes.ok:
        page_dom = BeautifulSoup(response.text, "html.parser")
        opinions = page_dom.select("div.js_product-review")
        for opinion in opinions:

            single_opinion = {}
            for key, value in selectors.items():
                single_opinion[key] = get_element(opinion, *value)
            single_opinion["recommendation"] = True if single_opinion["recommendation"] == "Polecam" else False if single_opinion["recommendation"] == "Nie polecam" else None
            single_opinion["score"] = np.divide(*[float(score.replace(",", ".")) for score in single_opinion["score"].split("/")])
            single_opinion["like"] = int(single_opinion["like"])
            single_opinion["dislike"] = int(single_opinion["dislike"])
            single_opinion["description"] = clean_text(single_opinion["description"])
            single_opinion["description_en"] = translator.translate(single_opinion["description"][:500])
            single_opinion["pros_en"] = translator.translate(single_opinion["pros"][:500])
            single_opinion["cons_en"] = translator.translate(single_opinion["cons"][:500])
            all_opinions.append(single_opinion)
        try:
            page = get_element(page_dom, "a.pagination__next","href")
            url = "https://www.ceneo.pl" + page
        except TypeError:
            url = None
if len(all_opinions) > 0:
    if not os.path.exists("./opinions"):
        os.mkdir("./opinions")
    with open(f"./opinions/{product_code}.json", "w",encoding="UTF-8") as jf:
        json.dump(all_opinions,jf,indent=4,ensure_ascii=False)