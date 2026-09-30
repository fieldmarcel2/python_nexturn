from flask import Flask, request
import requests
import json

app= Flask(__name__)

@app.get("/")

def get_home():

    return " home page"


URL = "https://dummyjson.com/products"

response = requests.get(URL)
data= response.json()

@app.get("/products/<product_name>")

def  get_products(product_name):
 prod=[]
 for i in data["products"]:
    if i["category"]== product_name:
       prod.append(i)

 else :
       return " no product listed "


 return prod   

if __name__== "__main__":

 app.run(debug= True)
