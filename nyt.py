import datetime

now = datetime.datetime.now()
print ("Current date and time : ")
print (now.strftime("%Y-%m-%d %H:%M:%S"))
with open("aika.txt", "a") as file:
    file.write(str(now))
    
    
