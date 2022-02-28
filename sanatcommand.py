# Import the library
import argparse
# Create the parser
parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('-f', '--file', type=str, required=True)
# Parse the argument
args = parser.parse_args()

try:
    with open("demo.txt") as tiedosto:
        lines = tiedosto.readlines()
        lines.sort(key = len)
except:
    print("Ei ole tiedostoa")
    
with open(args.file, "a") as uusitiedosto:
    for i in lines:
        uusitiedosto.write(i)
    
print(lines)