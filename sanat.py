



try:
    with open("demo.txt") as tiedosto:
        lines = tiedosto.readlines()
        lines.sort(key = len)
except:
    print("Ei ole tiedostoa")
    
with open("uusi.txt", "a") as uusitiedosto:
    for i in lines:
        uusitiedosto.write(i)
    
print(lines)