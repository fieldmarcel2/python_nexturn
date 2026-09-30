import json

# with open("./sample.json") as file:

#     data= json.load(file)

#     print(data)
#     print(data[0]["college"])
#     print(type(data))



# q total price
# q  most expensive and cheapest item 
# create json for each product category
with open("./sample.json") as file:

    data= json.load(file)



# price =0

# for i in data:
#     price+=i['product_price']

# print(round(price,2))    



# x=0
# y=1e5
# item1=""
# item2= ""
# for i in data:


#  if( i["product_price"] >x):
#     x=i["product_price"]
#     item1=i['product']
# #  x =min(i["product_price"])

# #  y=max(i["product_price"])
#  if( i["product_price"] <y):
#     y=i["product_price"]
#     item2=i['product']
 


# print(item1 ,x)
# print(item2, y)

# print(f"{x} \n {y}")


# jsondata={}
# categories={}
# for i in data:
#  category= i["product_category"]
# if category not in categories:
#    categories[category]= []
#    categories[category].append("product")
   



# category = list(map(lambda x:x['product_category'],data))
# category =  set(category)


# for i in category:
#     filtered_items= list(filter(lambda x:x ['product_category']== i, data))
#     with open (f"../products/{i}.json",'w') as file:
#         json_string = json.dumps(filtered_items)

#         file.write(json_string)




    # take user input find if given keyword present in name or description

x= input("your item  ")


for i in data:
    #i need list for it  #if( i['product'].lower().split(" ")==x or i['product_description'].lower().split(" ")== x):
    if( x  in i['product'].lower() and x in i["product_description"].lower()):
        print(" your item is present and product is ", i["product"])
#    if you want to search for a word inside the product
        break

# Use in: