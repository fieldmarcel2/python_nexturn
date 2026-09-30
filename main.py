# print("hello world")

# print( 5+2)

# # print("5"+2)

# print("2" *5)

# print( "*" *1)
# print( "*" *2)
# print( "*" *3)
# print( "*" *4)
# print( "*" *5)

i="10"
j='10'
# print(type(i))
# print(type(j))
# # so char and str bit have same type str in python

# k=4.0
# print(type(k))

# i= input("what is your name\n")
# print(i)

# i= input("name")
# j= input("sirname")

# print(i+j)

# print( "hello"+" "+"world")


# i= input ("enter the no.")
# x=float(i)
# print(i ,"x 1" , "=" ,(x* int(1)))
# print(i ,"x 2" , "=" ,(x* int(2)))
# print(i ,"x 3" , "=" ,(x* int(3)))
# print(i ,"x 4" , "=" ,(x* int(4)))
# print(i ,"x 5", "=" ,(x* int(5)))
# print(i ,"x 6", "=" ,(float(i)* int(6)))
# print(i ,"x 7", "=" ,(float(i)* int(7)))
# print(i ,"x 8", "=" ,(float(i)* int(8)))
# print(i ,"x 9", "=" ,(float(i)* int(9)))
# print(i ,"x 10", "=" ,(float(i)* int(10)))


# i=10
# j=10.0

# if( i==j):
#     print("hello")
# else:
#     print("world")    

# i= input ("enter the no.")
# x=int(i)

# # if(x >=5 and x<=20):
# # if(5<=x<=20):
# if 5<=x <=20:
#     print("hello")
# else:
#     print("world")    



# if( x%2==0):
#     print("even")
# else:
#     print("odd")


# x= int(input( "enter the no."))

# if( x >=0 and x%2==0):
#         for i in range(x,0,-2):
#          print(i)

# elif(x<=0 and x%2==0):
#      for i in range (x,0, 2):
#       print(i)
# else : 
#      print("zero")



# j= "hello"
# for i in j:
#     print(i)


# x= int( input("enter the no "))
# temp=x
# sum=0
# z= len(str(x))
# while(x>0):
#     rem= x%10
#     y= int(pow(rem,z))
#     sum= sum+y
#     print(sum)
#     x=x //10


# if ( temp==sum):
#     print("true")
# else :print("false")    


secret=67
while True:
 x= int( input("enter the no."))
 if (x== secret):
  print ("u guessed the no.")
  break
 elif( x-10<= secret <= x+10):
  print("u r close")
 elif(x < secret):
  print( "not even close")
 else:
  print("bit too high")

