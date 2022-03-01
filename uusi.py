import os
import random
import string
import funktiot
from azure.identity import AzureCliCredential



credential = AzureCliCredential()
subscription_id = os.environ["SUBSCRIPTION_ID"]

kayttajanimi = str(input("Anna nimesi, resursseille luodaan nimet sen mukaan: "))
print("Luodaan käyttäjän parametrit")
with open("parametrit.py", "w") as parametrit:
    GROUP_NAME = f"{kayttajanimi}RG"
    STORAGE_ACCOUNT = f"{kayttajanimi}sa"
    BLOB_CONTAINER = f"{kayttajanimi}blobstorage"
    VIRTUAL_NETWORK_NAME = f"{kayttajanimi}VNET"
    blob_name = kayttajanimi + ''.join(random.choice(string.ascii_lowercase) for i in range(8))
    SUBNET_NAME = f"{kayttajanimi}Subnet"
    INTERFACE_NAME = f"{kayttajanimi}NIC"
    NETWORK_NAME = f"{kayttajanimi}VNET"
    OS_DISK = "disk" + ''.join(random.choice(string.ascii_lowercase) for z in range(8))
    NICSUBNET = "nic" + ''.join(random.choice(string.ascii_lowercase) for u in range(8))
    VM_NAME = kayttajanimi + ''.join(random.choice(string.ascii_lowercase) for x in range(8))
    your_password = 'A1_' + ''.join(random.choice(string.ascii_lowercase) for y in range(8))

    parametrit.write(f"GROUP_NAME = '{GROUP_NAME}'\n")
    parametrit.write(f"STORAGE_ACCOUNT = '{STORAGE_ACCOUNT}'\n")
    parametrit.write(f"BLOB_CONTAINER = '{BLOB_CONTAINER}'\n")
    parametrit.write(f"VIRTUAL_NETWORK_NAME = '{VIRTUAL_NETWORK_NAME}'\n")
    parametrit.write(f"blob_name = '{blob_name}'\n")
    parametrit.write(f"SUBNET_NAME = '{SUBNET_NAME}'\n")
    parametrit.write(f"INTERFACE_NAME = '{INTERFACE_NAME}'\n")
    parametrit.write(f"NETWORK_NAME = '{NETWORK_NAME}'\n")
    parametrit.write(f"OS_DISK = '{OS_DISK}'\n")
    parametrit.write(f"NICSUBNET = '{NICSUBNET}'\n")
    parametrit.write(f"VM_NAME = '{VM_NAME}'\n")
    parametrit.write(f"your_password = '{your_password}'")

    print(f"Salasanasi on {your_password}, ota talteen jos haluat päästä käsiksi VM.")


while True:
    syote = input(
    "Anna komento: 1: RG managerointi, 2: Storage managerointi, 3: VNet managerointi, 4: VM managerointi, X lopettaa :  ")
    if syote == "1":
        lisasyote = input("1: Luo RG, 2: Listaa RG:t, 3: Päivitä RG tageilla, 4: Poista RG, X: palaa : ")
        while lisasyote != "X":
            if lisasyote == "1":
                funktiot.createrg()
                break
            elif lisasyote == "2":
                funktiot.listrgs()
                break
            elif lisasyote == "3":
                taginimi = str(input("Anna tagin nimi: "))
                tagivalue = str(input("Anna tagin value: "))
                funktiot.updaterg(taginimi, tagivalue)
                break
            elif lisasyote == "4":
                funktiot.deleterg()
                break
            elif lisasyote == "X":
                break
            
    
        
    
    elif syote == "2":
        storagesyote = input(
            "1: Luo Storage Account, 2: Luo Blob Container, 3: Uploadaa tiedosto, 4: Lataa tiedosto, 5: Poista tiedosto, 6: Poista container, X: palaa : ")
        while storagesyote != "X":
            if storagesyote == "1":
                funktiot.createstorageacc()
                break
            elif storagesyote == "2":
                funktiot.createblobcont()
                break
            elif storagesyote == "3":
                funktiot.uploadfile()
                break
            elif storagesyote == "4":
                funktiot.downloadfile()
                break
            elif storagesyote == "5":
                funktiot.deletefile()
                break
            elif storagesyote == "6":
                funktiot.deletecontainer()
                break
            else:
                break
    elif syote == "3":
        vnetsyote = input("1: Luo VNET, 2: Luo Subnet, 3: poista Subnet, 4: poista VNET : ")
        while vnetsyote != "X":
            if vnetsyote == "1":
                funktiot.createvnet()
                break
            elif vnetsyote == "2":
                cidr = str(input("Anna CIDR, oletus 10.0.0.0/24"))
                funktiot.createsubnet(cidr)
                break
            elif vnetsyote == "3":
                funktiot.deletesubnet()
                break
            elif vnetsyote == "4":
                funktiot.deletevnet()
                break
    elif syote == "4":
        vmsyote = input(
            " 1: Luo NIC<PAKOLLINEN!>, 2: luo VM, 3: pysäytä VM, 4: käynnistä VM, 5: listaa VM:t, X: palaa : ")
        while vmsyote != "X":
            if vmsyote == "1":
                funktiot.createnic()
                break
            elif vmsyote == "0":
                funktiot.luosubnetnic()
                break
            elif vmsyote == "2":
                funktiot.createvm()
                break
            elif vmsyote == "3":
                funktiot.stopvm()
                break
            elif vmsyote == "4":
                funktiot.startvm()
                break
            elif vmsyote == "5":
                funktiot.listvm()
                break
    elif syote == "X" or syote == "x":
        break    