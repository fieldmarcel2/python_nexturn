
import math


class calculator:

    def sqrt(self, a):
        return math.sqrt(a)

    def factorial(self, b):
        return math.factorial(b)


from faker import Faker

fake = Faker()

    
class Person:

    def __init__(self ,name, city , country, phone, addr):
        self.name= name
        self.city= city
        self.country= country
        self.phone= phone
        self.addr= addr



persons=[]     

for i in range(0,50):

    p= Person(fake.name(), fake.city(), fake.country() , fake.phone_number(), fake.address())


    persons.append(p)


country_count={}

for i in persons:

    country= i.country

    if( country in country_count):
        country_count[country] +=1
    else :country_count[country] =1  

print(country_count)    

    
    # print(persons[i].name)

cities=set()
for i in persons:

 city= i.city
 country= i.country

 cities.add(f"{city} : {country}")     


print(cities)