file= open("sample.txt")

log= file.read()


info=0
error=0
warning=0

for i in log:

    if "info" in log :
        info+=1
