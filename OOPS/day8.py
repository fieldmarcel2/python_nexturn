class Car:

    def start(self):
        self.__check_engine() #private called
        print("Car started")

    def __check_engine(self):  #private 
        print("Checking engine...")


c1 = Car()

c1.start()





# inheritence

class car:
    def __init__(self,doors):
        self.doors= doors


    def sound(self):
        print("vroom vroom")

    def __breaking(self):
        print("stop")


class I20(car):
    def acc(self):
        print("cars going fast")

c1= I20(4)

c1.sound()
c1.acc()
print(c1.doors)


#hybrid inheritence



class A:

    def grey_hairs(self):
     print("this is grandparent1 functiom")


class B:

    def grey_hairs(self):
     print("this is grandparent2 functiom")



class parent(B,A):   #order matters here a,b  or b,a
   def eyesight(self):
      print(" child of A,B")
     


class child(parent):
   def fit(self):
      print(" child of parent")



c1= child()

c1.eyesight()
c1.fit()
c1.grey_hairs()


# diamond problem
    #     Animal
    #    /      \
    #  Dog      Cat
    #    \      /
    #      Pet

class Animal:

    def sound(self):
        print("animal sound")


class Dog(Animal):

    def sound(self):
        print("bhowww")


class Cat(Animal):

    def sound(self):
        print("meowww")


class Pet( Dog,Cat):

    def speak(self):
        print("which one?")


p1 = Pet()

p1.sound()



def make_sound(animal):
    animal.sound()


dog = Dog()
cat = Cat()

make_sound(dog)
make_sound(cat)



#polymorphism with inheritence 
class Animal:

    def sound(self):
        print("Animal makes sound")


class Dog(Animal):

    def sound(self):
        print("Bhow bhow")


class Cat(Animal):

    def sound(self):
        print("Meow meow")


animals = [Dog(), Cat(), Animal()]

for animal in animals:
    animal.sound()






#abstraction

from abc import ABC,abstractmethod



class Animal(ABC):

    @abstractmethod
    def sound(self):
        pass


class Dog(Animal):

    def sound(self):
        print("Bhow bhow")


class Cat(Animal):

    def sound(self):
        print("Meow meow")


d1 = Dog()
c1 = Cat()

d1.sound()
c1.sound()

# 1. ABC
# class Animal(ABC):

# ABC stands for Abstract Base Class.

# We're saying:

# Animal is going to be an abstract class that defines what its child classes should do.

# 2. @abstractmethod
# @abstractmethod
# def sound(self):
#     pass

# This means:

# Every concrete child class must provide its own implementation of sound().

# So Animal basically says:

# "Every animal should have a sound() method, but I don't care how you implement it."

# That's abstraction.
#                 Animal
#            (abstract class)
#                   │
#           ┌───────┴───────┐
#           ↓               ↓
#          Dog             Cat
#           │               │
#      sound()            sound()
#        ↓                   ↓
#    "Bhow bhow"         "Meow meow"
# The parent class says:

# "Every animal MUST have sound()."

# But it doesn't decide what the sound is.

# The child classes decide.

