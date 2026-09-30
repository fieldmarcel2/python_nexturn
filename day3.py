import math

math.pi= "shivanshu"

print(math.pi)



def sum(a, b):

    return a+b


def func(x):

    ans= x

    print(ans)


# a= int(input("a "))
# b= int(input("b "))
# func(sum(a,b))



# my_list=[10,20,5,6,70,80]

# def filter_func(item):
#     if item <10:
#         return True
#     else :False

#     op= list(filter(filter_func, my_list))
#     print(op)


foods=['banana', 'apple', 'biryani','pizza']


# def filter_food(items):

#     if items.count("i") >= 2:
#         return True  
#     #or -11 -12 anything intead of 0 none false  it will return the data
#     else :
#         return False


# # filter(function, iterable)

# output= list(filter(filter_food, foods)) 


# print(output)


wishlist={
"foods":['banana', 'apple', 'biryani','pizza white'],
"bike":["royal enfield", "MV Augusta"],
"cars":['Toyota LC 300' , "BMW m5"],
} 


# for key ,val in wishlist.items():

#    print(key)
#    print(val)



# def wishfunc(items):


#   if items.count(" ")>0:
#      return True

#     # for x in values:
#     #   if " " in x:
#     #     return True
#     # else: return False 

# for key , val in wishlist.items():
#    wishlist[key]= list(filter(wishfunc, wishlist))

# op= dict(filter( wishfunc, wishlist.items()))   
# print(op)




# ======== strings=======

my_text= "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since 1966, when designers at Letraset and James Mosley, the librarian at St Bride Printing Library in London, took a 1914 Cicero translation and scrambled it to make dummy text for Letraset's Body Type sheets. It has survived not only many decades, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised thanks to" \
" these sheets and more recently with desktop publishing software like Aldus PageMaker and Microsoft Word including " \
"versions of Lorem Ipsum."

vow= my_text.count("a") + my_text.count("e") + my_text.count("i") + my_text.count("o") + my_text.count("u")
print(vow)

total= my_text.count("")
print(total-vow)

cnt=0
cap=0
for i in my_text:
    if(i.islower()) :cnt+=1
    elif(i.isupper()):cap+=1

print(cnt, cap)

space= my_text.count(" ")
print(space)

print(ord("A"))



# txt= ("aa aa" )
# cnt=0

# x=[]

# for i in txt:

#  if( i== " "):
#     x.append(cnt)
#     cnt=0
#  elif(i !=" "):
#   cnt= cnt+ ord(i)

# x.append(cnt) 


# print(x) 



# text= "abcde"

