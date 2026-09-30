# print("[x][][][]")

# from database import books

# temp=[]
# def check_year(books):
#     return books["year"] <= 1890


# temp = list(filter(check_year, books))

# print(temp)


# count=0
# for i in books:
#    if "Russian" in i["description"]:
#       count+=1
#       print(i['title'])



# print(count)

# # create a dict of genre wise book titles
# dict={}
# horror=[]
# action=[]
# Gothic=[]
# Psychological=[]

# lists={}
# for i in books:
#    genre= i['genre']


#    if genre in lists:
#        lists[genre].append(i['title'])
#    else: lists[genre]= [i["title"]]
   

# print(lists)

# # create a list of dict where each item (dict) will contain 
# # [


# #    {
# #       author "mary shelley"
# #       "books":{},
# #       ]
# #    }
# # ]


# # key={
# # "a":"fffs",
# # "d":"sdfs",
# # "f":"awr",
# # "d":"iueyr",
# # "e":"djgu",
# # "o":"dshk",
# # "w":"sdf"
# # }

# # for i in key:




# my_list= [[1,2,3,4,5], 
#           [1,[23,34,5,6,[1,3,4,5,[2345]]]],5,6,7,8,0,30,[20,40,[[20]]]]


my_str = "abcdefgrh"
x=""
for i in my_str:
    if( ord(i) %2 !=0):
      x+=(i)


print(x)