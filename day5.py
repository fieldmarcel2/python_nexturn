# x=[1,2,3,4] #//stack

# def pushed(list,item):
#  ( list.append(item))
#  return list


# print( pushed(x,5))

# def popx(list):


#  if len(list)==0:
#   print ("no pop")
#   return list
#  else: 
#   return list,list.pop()

# print( popx(x))


# def clear():
#  list.clear()




# queue=[1,2,3,4]

# def pushed(queue, item):
#     queue.append(item)
#     return queue


# def popx(queue):
#     if len(queue) == 0:
#         print("No item to pop")
#         return queue
#     else:
#         popped_item = queue.pop(0)
#         return popped_item


# def display(queue):
#     print(queue)


# def clear(queue):
#     queue.clear()
#     print("Queue cleared")


# if __name__ == "__main__":

#     queue = []

#     while True:

#         print("\n1. Push")
#         print("2. Pop")
#         print("3. Display")
#         print("4. Clear")
#         print("5. Exit")

#         choice = int(input("Enter your choice: "))

#         match choice:

#             case 1:
#                 item = input("Enter the data: ")
#                 pushed(queue, item)
#                 print("Queue:", queue)

#             case 2:
#                 popped_item = popx(queue)
#                 print("Popped:", popped_item)

#             case 3:
#                 display(queue)

#             case 4:
#                 clear(queue)

#             case 5:
#                 print("Exiting...")
#                 break

#             case _:
#                 print("Invalid choice")




block1 = {"item": "sampleitem1", "next": None, "prev": None}
block2 = {"item": "sampleitem2", "next": None, "prev": None}
block3 = {"item": "sampleitem3", "next": None, "prev": None}
block4 = {"item": "sampleitem4", "next": None, "prev": None}
block5 = {"item": "sampleitem5", "next": None, "prev": None}


block1["next"] = block2
block2["next"] = block3
block3["next"] = block4
block4["next"] = block5
block5["next"] = block1


block1["prev"] = block5
block2["prev"] = block1
block3["prev"] = block2
block4["prev"] = block3
block5["prev"] = block4




curr= block1
# curr['next']= block2
# " x= [x][][][][]"

while True:
    

    print(curr['item'])

    curr= curr['next']
    if( curr == block1):
        break


curr= block5
while True:
        print(curr['item']) 
        curr= curr['prev']

        if ( curr ==block5):
             break



import os

print(os.getcwd())

from datetime import datetime



employee = [
   {"name": "Ron", "joiningDate": "12-06-2004", "inHand": "4,00,000"},
   {"name": "Tom", "joiningDate": "11-04-2012", "inHand": "3,00,000"},
   {"name": "Jan", "joiningDate": "10-04-2012", "inHand": "6,00,000"},
   {"name": "Jerry", "joiningDate": "02-06-2004", "inHand": "3,20,000"},
   {"name": "Sean", "joiningDate": "12-07-2004", "inHand": "6,10,000"}
]


senior= employee[0]
junior= employee[0]
for i in employee:

     currentDate =datetime.strptime(i["joiningDate"] ,"%d-%m-%Y")


     seniorDate = datetime.strptime(senior["joiningDate"], "%d-%m-%Y")

     if( currentDate <seniorDate):
          senior= i

     juniorDate= datetime.strptime(junior['joiningDate'], "%d-%m-%Y")
     if( currentDate >juniorDate):
          junior=i




          print( datetime)
print(senior , junior)          

# date_shiva= datetime(2005, 3,4)

# print( date_shiva.strftime("%a/%d/%B/%Y"))