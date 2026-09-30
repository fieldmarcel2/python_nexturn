# def print_hello():
#     print("hello world")


# print_hello()    

class my_firstClass:

    def say_hello(self):
        print("hello shivanshu")


    def sayhello2(self,a,b):
        return a+b

obj1 = my_firstClass()

obj1.say_hello()

print(obj1.sayhello2(3,4))

from cal import calculator   #from filename import classname

# class calculator:

#     def sqrt(self, a):
#         return math.sqrt(a)

#     def factorial(self, b):
#         return math.factorial(b)



obj= calculator()

print(obj.sqrt(16))
print(obj.factorial(5))


# crete a stuent class with fol data memebers
# 1. name 
# 2. usn
# 3. attendance(att) 
# all these compulsory


# 2 make  a lsit of student objects 
# 3 find out student with with ma and min att

#     4 a min of 2 students must be there in the list

class student:
     def __init__( self , name, usn , att):
         self.name= name
         self.usn= usn
         self.att = att


s1= student("Shivanshu" , "122ec0038", 75)
s2= student("Tripathi" , "122ec0038", 85)
s2= student("xyzx" , "122ec0039", 45)


students=[ s1,s2]


maxi = max( students, key=lambda x: x.att)
mini= min( students, key=lambda x: x.att)


ma= students[0].att
mi = students[0].att
# for i in range(len(students)):

   

# print(s1.name)
# print(s1.usn)

# print(s1.att)

print(maxi.att)
print(mini.att)


students = [
    {"name": "Rishabh Verma", "usn": "USN001", "att": 92},
    {"name": "Aman Sharma", "usn": "USN002", "att": 85},
    {"name": "Priya Singh", "usn": "USN003", "att": 78},
    {"name": "Rahul Kumar", "usn": "USN004", "att": 88},
    {"name": "Sneha Patel", "usn": "USN005", "att": 95},
    {"name": "Arjun Reddy", "usn": "USN006", "att": 72},
    {"name": "Neha Gupta", "usn": "USN007", "att": 90},
    {"name": "Vikram Rao", "usn": "USN008", "att": 81},
    {"name": "Anjali Mehta", "usn": "USN009", "att": 87},
    {"name": "Karan Joshi", "usn": "USN010", "att": 76}
]

# lists_obj=[]

# for stud in students:
#     lists_obj= [stud.name , stud.usn , stud.att]



# print(lists_obj)


# // create 2 class 
# 1 person ->monthly_salary, name str , monthlyexpense:list(expenseitem), 
# memberfn ->remainign bank balaance

# 2 expenseitem-> expense_name:str ,m expense_amount:float


class person:
    def __init__( self , name , month_sal , month_exp):
        self.name= name
        self.month_sal= month_sal
        self.month_exp= month_exp


    def rem_bal( self ):   #member fn
        return  self.month_sal- self.month_exp 
            

class expenseitem:

    def __init__(self , exp_name,exp_amount):
        self.exp_name= exp_name
        self.exp_amount= exp_amount



s1= person("shiva", 50000, 30000) #s1  is creation of object
s2= person( "tripathi", 80000, 50000)

print( s1.rem_bal())




# setter and getter


class sampleClass:


  def  __init__ (self, name,usn, university):
     self.name= name
     self.usn = usn
     self.university= university


  def __str__(self):  #magic fn
     return f"student name {self.name}\n usn {self.usn}\n university {self.university}"   

     
     def set_age(self, age):
         self.age= age


     def get_age(self):
         return self.age     



s1= sampleClass(name="harry" , usn="007" , university="IIITDM KURNOOL")
print(s1)



# 1.class name, phoe, country , city, address
# 2 list of person with at least 50 entries
# 3
# give me countrywise frequency

 # 4 list of unique city in format :city, country eg hyderabad , india