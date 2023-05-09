import os
import pandas as ps
from matplotlib import pyplot as plt

print(*[filename.split(".")[0]for filename in os.listdir("./options")], sep="\n")

product_code = input("Please enter the product code: ")

options = ps.read_json(f" ./opinions/{product_code}.json")
print(opinions)

opinions_count = opinions.shape[0]
pros_count = 0
cons_count = 0
average_score = 0

print(f"""For the product with the {product_code} code 
there is {opinions_count} opinions posted.
for {pros_count} opinions the list of product advantages is given
and for {cons_count} opinions the list of product disadvantages is given. """)


recommendations = opinions.recommendation.value_count(dropna=False)

