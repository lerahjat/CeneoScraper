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
            single_opinion = {

            }
    else:    
         print(f"There are no opinions about product with {product_code}code.")
print(response.status_code)