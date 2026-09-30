#create a dynamic route /<category>
#where category is product_category
#n represent how much data to respond
 #/category ->all the items in that category


from flask import Flask , request
import json

app= Flask(__name__)


with open ("../sample.json") as file:
    data= json.load(file)



@app.get("/<category>")

def handle_category(category):

 category= category.lower()

#  data= response.json()
 prod=[]
 for i in data:
     if i["product_category"].lower() == category:
    #  if i.get("product_category", "").lower() == category:

       prod.append(i)

     if not i:
      return ({
            "message": f"No products found in category '{category}'",
            "category": category,
            "count": 0
        }), 404 
 return ({
        "category": category,
        "count": len(prod),
        "products": prod
    })


# @app.get("/<caregory>/<int:n>")


if __name__== "__main__":
 app.run(debug= True)