

# lambda fn
# x= int(input("input here x : "))
# y= int( input( " input here y "))
# z= int( input( " input here z "))

# data= (lambda a: (x**3))
# print(data(x))

# data = (lambda x: "true" if x%2==0 else "false")
# print(data(x))

# But lambda functions use a "ternary operator" which flips the order.
# Incorrect: if condition value else alternative
# Correct: value if condition else alternative

# Q4. Find maximum of two numbers
# data = (lambda x,y,z : x if x<y<z  else (y if y<x<z else z) ) #no elif just nested if else
# data = lambda x,y,z : min(x,y,z)
# print(data(x,y,z))

# F = (C × 9/5) + 32

# c= int(input(" enter degree  "))

# data= lambda c: ((c*9/5) + 32)

# print(data(c))


# map(function, list)###############################

# numbers = [1, 2, 3, 4, 5]
# data=[]
# data=  list( map( lambda x: x**4, numbers))

# print( data)
# Wrapping it in list() tells Python to run the math on every item 
# right now and pack them into a standard list.

# names = ["rahul", "shiva", "rohit", "aman"]
# words = ["python", "flask", "aws", "database"]
# data= list(map(lambda x: x.upper(), names))
# data2= list(map(lambda x: len(x), words))
# print(data2)

# data2=[]
# def  getlen(x):

#     for i in x:
#         data2.append([len(i)])

# getlen(words)
# print(data2)

numbers = [5, 10, 15, 20]

data3= list(map(lambda x: x+10, numbers))
print(data3)

numbers2 = ["10", "20", "30", "40"]
data4= list(map(lambda x: int(x), numbers2))

print(data4)

names = ["Shivanshu", "Rahul", "Aman", "Rohit"]

data5 = list(map(lambda x: x[0], names))
print(data5)

numbers3 = [1, 2, 3, 4, 5, 6, 7, 8]

data6= list(filter( lambda x: x%2!=0 , numbers3))

print(data6)

numbers4 = [3,10, 55, 32, 80, 100, 45]

data7=  list( filter( lambda x: x%5==0, numbers4))
print(data7)

names2 = ["Aman", "Rahul", "Ankit", "Shiva", "Ajay"]
data8= list(filter(lambda x:x[0]=="A", names2))
print(data8)

words2 = ["python", "java", "flask", "database", "api", "developer"]

data9= list( filter(lambda x: len(x)>5, words2))

print(data9)


marks = [35, 78, 42, 29, 90, 55, 31]
data10= list(filter( lambda x: x>40, marks))

print(data10)


# In almost every case, you should use filter() before map(). means
#means filter inside then map outside
numbers5 = [1, 2, 3, 4, 5, 6, 7, 8]

data11= list( map(lambda x: x**2, filter(lambda x:x%2==0,numbers3)))

print(data11)

numbers6 = [5, 12, 8, 20, 25, 3]

data12= list(map(lambda x: x*2,(filter(lambda x: x >10,numbers6))))

print(data12)

numbers7 = [-5, 2, -3, 4, 0, 6]

data13 = list(map(lambda x: x*3 , filter( lambda x: x>0,numbers7)))
print(data13)


names3 = ["Rah", "Shivanshu", "Aman", "Rohit", "Alexander"]

data14 = list( map( lambda x: x.upper(), filter(lambda x: len(x)>=5, names3)))

print(data14)

numbers8 = [1, 2, 3, 4, 5, 6]

data15 = list( map( lambda x: x*10 , filter( lambda x: x%2==0, numbers8)))

print(data15)