my_list= [1,2,3,4,5,True,"hello"]
print(my_list[-1])
#//to get last index value fo list or array
# my_list.append(20)
print(my_list)

print(my_list[0:4]) #1,2,3 [index 0 to 2]
# its slicing left side closed and right side opended so we dont count last index 
print(my_list[3:6])
print(my_list[-5:-2])

my_list.extend(my_list)
new_list=[]
# print(my_list)

# print(my_list[4:8])

# print(my_list[::]) #whole list

# print(my_list[::2]) alternate of 2 intervals

# print(my_list[::-1]) #reverses the list

for i in my_list:

    # if( type(i) ==int):
    #    i=i*i;
    #    print(i)

    if(isinstance(i, int) or isinstance(i, float)):
        new_list.append(i**3)

print(new_list)

list1= [100,21.11,30.5, 42,55]
high=-1e6
low= 1e6
for i in list1:
    if( high < int(i) or high <float(i)):
        high= i

    if( low >int(i) or low >float(i)):
                low=i
        

print(high)
print(low) 


# sort ascending
# sort(reverse=True) descending

# tuples------immutable  very faster than list

# my_tuple=(1,2,3,4,5) tuple
# my_tuple=(1)  INT   important
my_tuple=(1,)  #tuple

# print(type(my_tuple))

list2= [2,3,1,4.2,5,6,7.5,8,9,10]


# asc=[]
# dsc=[]
# for i in list2:

#       if( i%2==0):
#            asc.append(i)
#       else :
#             dsc.append(i) 

# asc.sort()
# dsc.sort(reverse=True)
# print(asc,dsc)



# fisher yetes shuffle algorithm 


cards= [1,2,3,4,5,6]

import random

for i in range (len(cards)-1):
      random_no= random.randint(0, len(cards)-1)

      while(random_no == i):
      
        random_no= random.randint(0, len(cards)-1)

if (random_no != i) :
 cards[i], cards[random_no]= cards[random_no],cards[i]

print(cards)      



list3=[2,3,4,5,3,2,1]

for i, no in enumerate(list3):
     print( i, no) #to get both index and value




#====================     #FUNCTIONS============================



def my_func(a,b):

#  if type(a) is int and type(b)is int:
 if a.isdigit() and b.isdigit():
     print(a + b)
     print(a - b)
     print(a * b)
     print(a // b)




# a=float(input(" enter the no a "))
# b=float(input(" enter the no b "))


# ans = my_func(a,b)

# 5 / 2 → 2.5  true div
# 5 // 2 → 2 floor div


def area(side1, side2, shape):

    if( shape== "circle"):
     return 3.14*side1*side1

    elif( shape== "quad"):
             return side1*side2

    else :
        print("shape unrecognized")
    



def per(side1, side2, shape):

        if( shape== "circle"):
         return 2*3.14*side1
    
        elif( shape== "quad"):
        
         return 2*(side1+side2)
        else :
            print("shape unrecognized")

# shape= input("what is the shape ")
# side1= float(input("what is len"))
# side2= float(input("what is br"))

# ans= print(area(side1, side2, shape))
# ans= print(per(side1, side2, shape))


# =========DICTIONARY======

#in dictionary ..keys can only be strings
#can also be nested in nature

database= {
    "name": "shivanshu",
    "age": 22
}

print(database['name'])


# * rep a tuple of parameters
# ** named/keyword arguments (kwargs)

# def func(*args):
#     print(args)

# func(2,3,4,5,6,7)

def print_table(a, order):


 if (order == "reverse"):
  for i in range( 10,0,-1):
    print( a,"X",i,"=",a*i )

 else :
  for i in range( 1,11,1):
    print( a,"X",i,"=",a*i )



# a= int(input("enter the no  "))
# userorder= input("enter order  ")

# (print_table(a, order= userorder))





emp=[
    {"name": "Ron","joiningDate":"12-06-2004","inHand":"4,00,000"},
    {"name": "Ron","joiningDate":"12-06-2005","inHand":"5,00,000"},

    {"name": "Ron","joiningDate":"12-06-2006","inHand":"6,00,000"},

    {"name": "Ron","joiningDate":"12-06-2007","inHand":"7,00,000"}


]

def cleansalary(empdict):
    return int(empdict["inHand"].replace(",",""))


highest=  max(emp, key=cleansalary)
lowest=  min(emp, key=cleansalary)



# def sumsal():
#    sum=0
#    for inHand in emp:
#       sum +=int(inHand)


#    return sum


print( highest)
print( lowest)