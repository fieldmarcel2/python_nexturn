# lambda fn
# ternary operator





#longest running sequence

# text= "aerederabcd"
# cnt=0
# str= ""
# for i in range(1, len(text)):
        
#   if( ord(text[i])== ord(text[i-1])):
#         cnt=+1
#         if cnt>=len(str):
      

from joke import joke



# res= joke.random_10()

# for i in range (len(res)-6):
    
#   print(res[i]["question"])
#   print(res[i]["answer"])





# =====sets

#[:] #slicing

my_set={ 1,2,3,4,2,5,6,7,2}

print(my_set)

my_set.pop()

print(my_set)


my_list=[1,2,3,4,5,6,7,8]
#map()

def map_func(items):
      return items+1

print(list(map(map_func,my_list)))


listx= [

      {"name":"harry","usn":"007"},
            {"name":"potter","usn":"007"},

      {"name":"voldemart","usn":"007"},

      {"name":"harry","usn":"007"}
      ]


def mapfunc(items):

 if( "name" in items and items["name"] =="harry"):
   return "true"      
 else:
     return("false")
  
print((list(filter(mapfunc, listx))))

# print(list(map(lambda items: items["name"], listx)))