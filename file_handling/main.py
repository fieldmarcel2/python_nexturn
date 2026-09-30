# count following -->
# no of words
# no of lines
# no of empty lines
# print the char freqnecy (ignore special chars)
#find the most common word in the file

with open("./horror_story.txt") as file:
    story= file.read()

    word_list = story.split()
    print( len(word_list))

# word_list = story.replace("\n\n", " ").replace("\n", " ").split(" ")

lines= story.split("\n")

print(len(lines))
x=0

for line in lines:
   if line.strip()=="":
      x +=1
print(x)   

# emptylines= story.split("\n\n")
# print(len(emptylines))
#     split() without an argument automatically handles:

# spaces
# \n
# \t
# multiple spaces
# multiple newlines

# .strip()

# strip() removes whitespace from both ends of a string.



dicts={}
for i in story:
   if i.isalnum():
       
       i= i.lower()
       if i in dicts:
           
        dicts[i]+=1

       else :dicts[i]=1    



print(dicts)