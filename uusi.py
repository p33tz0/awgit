import os
import os
import random
import string

from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.storage.blob import BlobClient
from azure.storage.blob import BlobServiceClient

kayttajanimi = str(input("Anna nimesi, resursseille luodaan nimet sen mukaan: "))
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
VM_NAME = kayttajanimi + ''.join(random.choice(string.ascii_lowercase) for u in range(8))

your_password = 'A1_' + ''.join(random.choice(string.ascii_lowercase) for y in range(8))

credential = AzureCliCredential()
subscription_id = os.environ["SUBSCRIPTION_ID"]
resource_client = ResourceManagementClient(credential, subscription_id)
storage_client = StorageManagementClient(credential, subscription_id)
network_client = NetworkManagementClient(credential, subscription_id)
compute_client = ComputeManagementClient(credential, subscription_id)


def listrgs():
    # Retrieve the list of resource groups
    group_list = resource_client.resource_groups.list()

    # Show the groups in formatted output
    column_width = 40

    print("Resource Group".ljust(column_width) + "Location")
    print("-" * (column_width * 2))

    for group in list(group_list):
        print(f"{group.name:<{column_width}}{group.location}")


def createrg():
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "westeurope"})


def getrg():
    # Get resource group
    resource_group = resource_client.resource_groups.get(
        GROUP_NAME
    )
    print("Get resource group:\n{}".format(resource_group))


def updaterg(taginimi, tagivalue):
    # Update resource group
    resource_group = resource_client.resource_groups.update(
        GROUP_NAME,
        {
            "tags": {
                taginimi: tagivalue,
            }
        }
    )
    print("Update resource group:\n{}".format(resource_group))


def deleterg():
    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()
    print("Delete resource group.\n")


def createstorageacc():
    # Create storage account
    storage_client.storage_accounts.begin_create(
        GROUP_NAME,
        STORAGE_ACCOUNT,
        {
            "sku": {
                "name": "Standard_GRS"
            },
            "kind": "StorageV2",
            "location": "eastus",
            "encryption": {
                "services": {
                    "file": {
                        "key_type": "Account",
                        "enabled": True
                    },
                    "blob": {
                        "key_type": "Account",
                        "enabled": True
                    }
                },
                "key_source": "Microsoft.Storage"
            },
            "tags": {
                "key1": "value1",
                "key2": "value2"
            }
        }
    ).result()
    # - end -


def createblobcont():
    # Create blob container
    blob_container = storage_client.blob_containers.create(
        GROUP_NAME,
        STORAGE_ACCOUNT,
        BLOB_CONTAINER,
        {}
    )
    print("Create blob container:\n{}".format(blob_container))


def uploadfile(nimi="Default.txt"):
    MY_CONNECTION_STRING = str(input("Anna connection string Blob containeriin: "))
    BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)
    blob = BlobClient.from_connection_string(MY_CONNECTION_STRING, BLOB_CONTAINER, nimi)
    with open(nimi, "rb") as data:
        blob.upload_blob(data)


def downloadfile(nimi="Default.txt"):
    MY_CONNECTION_STRING = str(input("Anna connection string Blob containeriin: "))
    BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)
    blob = BlobClient.from_connection_string(MY_CONNECTION_STRING, BLOB_CONTAINER, nimi)
    with open(nimi, "wb") as my_blob:
        blob_data = blob.download_blob()
        blob_data.readinto(my_blob)


def deletefile(nimi="Default.txt"):
    MY_CONNECTION_STRING = str(input("Anna connection string Blob containeriin: "))
    BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)
    blob = BlobClient.from_connection_string(MY_CONNECTION_STRING, BLOB_CONTAINER, nimi)
    blob.delete_blob(delete_snapshots=False)


def deletecontainer(nimi):
    blob_container = storage_client.blob_containers.delete(
        GROUP_NAME,
        STORAGE_ACCOUNT,
        nimi
    )
    print("Delete blob container.\n")


def listvnet():
    result_create = network_client.virtual_networks.list(
        GROUP_NAME,
    )
    for re in result_create:
        print(re.name)


def createvnet(nimi="defaultvnet"):
    # Create virtual network
    network = network_client.virtual_networks.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME,
        {
            "address_space": {
                "address_prefixes": [
                    "10.0.0.0/16"
                ]
            },
            "location": "westeurope"
        }
    ).result()
    print("Create virtual network:\n{}".format(network))


def createsubnet(subnetCIDR):
    # Create subnet
    subnet = network_client.subnets.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME,
        SUBNET_NAME,
        {
            "address_prefix": subnetCIDR
        }
    ).result()
    print("Create subnet:\n{}".format(subnet))


def deletesubnet():
    # Delete subnet
    subnet = network_client.subnets.begin_delete(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME,
        SUBNET_NAME
    ).result()
    print("Delete subnet.\n")


def deletevnet(nimi="defaultvnet"):
    network = network_client.virtual_networks.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME)

def luosubnetnic():
    async_subnet = network_client.subnets.begin_create_or_update(
        GROUP_NAME,
        NETWORK_NAME,
        NICSUBNET,
        {'address_prefix': '10.1.0.0/24'}
    )
    async_subnet.wait()

def createnic():


    # Create network interface
    network_client.network_interfaces.begin_create_or_update(
        GROUP_NAME,
        INTERFACE_NAME,
        {
            'location': "westeurope",
            'ip_configurations': [{
                'name': 'MyIpConfig',
                'subnet': {
                    'id': str(f"/subscriptions/{subscription_id}/resourceGroups/{GROUP_NAME}/providers/Microsoft.Network/virtualNetworks/{VIRTUAL_NETWORK_NAME}/subnets/{SUBNET_NAME}")
                }
            }]
        }
    ).result()


def createvm():
    NICNIMI = "nic" + ''.join(random.choice(string.ascii_lowercase) for u in range(8))
    network_client.network_interfaces.begin_create_or_update(
        GROUP_NAME,
        NICNIMI,
        {
            'location': "westeurope",
            'ip_configurations': [{
                'name': 'MyIpConfig',
                'subnet': {
                    'id': str(
                        f"/subscriptions/{subscription_id}/resourceGroups/{GROUP_NAME}/providers/Microsoft.Network/virtualNetworks/{VIRTUAL_NETWORK_NAME}/subnets/{SUBNET_NAME}")
                }
            }]
        }
    ).result()

    vm = compute_client.virtual_machines.begin_create_or_update(
        GROUP_NAME,
        VM_NAME,
        {
            "location": "westeurope",
            "hardware_profile": {
                "vm_size": "Standard_D2_v2"
            },
            "storage_profile": {
                "image_reference": {
                    "sku": "2016-Datacenter",
                    "publisher": "MicrosoftWindowsServer",
                    "version": "latest",
                    "offer": "WindowsServer"
                },
                "os_disk": {
                    "caching": "ReadWrite",
                    "managed_disk": {
                        "storage_account_type": "Standard_LRS"
                    },
                    "name": OS_DISK,
                    "create_option": "FromImage"
                },
                "data_disks": [
                    {
                        "disk_size_gb": "1023",
                        "create_option": "Empty",
                        "lun": "0"
                    },
                    {
                        "disk_size_gb": "1023",
                        "create_option": "Empty",
                        "lun": "1"
                    }
                ]
            },
            "os_profile": {
                "admin_username": "testuser",
                "computer_name": "myVM",
                "admin_password": your_password,
                "windows_configuration": {
                    "enable_automatic_updates": True  # need automatic update for reimage
                }
            },
            "network_profile": {
                "network_interfaces": [
                    {
                        "id": "/subscriptions/" + subscription_id + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/networkInterfaces/" + NICNIMI + "",
                        # "id": NIC_ID,
                        "properties": {
                            "primary": True
                        }
                    }
                ]
            }
        }
    ).result()
    print("Create virtual machine:\n{}".format(vm))


def stopvm(nimi=VM_NAME):
    # Stop the VM
    print('\nStop VM')
    async_vm_stop = compute_client.virtual_machines.begin_power_off(
        GROUP_NAME, VM_NAME)
    async_vm_stop.wait()


def startvm(nimi=VM_NAME):
    # Start the VM
    print('\nStart VM')
    async_vm_start = compute_client.virtual_machines.begin_start(
        GROUP_NAME, VM_NAME)
    async_vm_start.wait()


def listvm():
    result_create = compute_client.virtual_machines.list(
        GROUP_NAME,
    )
    for re in result_create:
        print(re.name)


def valitsin():
    syote = input(
        "Anna komento: 1: RG managerointi, 2: Storage managerointi, 3: VNet managerointi, 4: VM managerointi:  ")
    while syote != "X":
        if syote == "1":
            lisasyote = input("1: Luo RG, 2: Listaa RG:t, 3: Päivitä RG tageilla, 4: Poista RG, X: palaa: ")
            while lisasyote != " ":
                if lisasyote == "1":
                    createrg()
                    break
                elif lisasyote == "2":
                    listrgs()
                    break
                elif lisasyote == "3":
                    taginimi = str(input("Anna tagin nimi: "))
                    tagivalue = str(input("Anna tagin value: "))
                    updaterg(taginimi, tagivalue)
                    break
                elif lisasyote == "4":
                    deleterg()
                    break
                elif lisasyote == "X":

                    break
            else:
                break
        elif syote == "2":
            storagesyote = input(
                "1: Luo Storage Account, 2: Luo Blob Container, 3: Uploadaa tiedosto, 4: Lataa tiedosto, 5: Poista tiedosto, 6: Poista container, X: Palaa")
            while storagesyote != "X":
                if storagesyote == "1":

                    createstorageacc()
                    break
                elif storagesyote == "2":

                    createblobcont()
                    break
                elif storagesyote == "3":
                    filenimi = str(input("Anna tiedoston nimi, tyhjänä oletus: "))
                    uploadfile(filenimi)
                    break
                elif storagesyote == "4":
                    latausnimi = str(input("Anna tiedoston nimi, tyhjänä oletus: "))
                    downloadfile(latausnimi)
                    break
                elif storagesyote == "5":
                    deletenimi = str(input("Anna tiedoston nimi, tyhjänä oletus: "))
                    deletefile(deletenimi)
                    break
                elif storagesyote == "6":
                    deletecontainersyote = str(input("Anna containerin nimi, tyhjänä oletus: "))
                    deletecontainer(deletecontainersyote)
                    break
            else:
                break
        elif syote == "3":
            vnetsyote = input("1: Luo VNET, 2: Luo Subnet, 3: poista Subnet, 4: poista VNET")
            while vnetsyote != "X":
                if vnetsyote == "1":

                    createvnet()
                    break
                elif vnetsyote == "2":
                    cidr = str(input("Anna CIDR, oletus 10.0.0.0/24"))
                    createsubnet(cidr)
                    break
                elif vnetsyote == "3":
                    deletesubnet()
                    break
                elif vnetsyote == "4":

                    deletevnet()
                    break
            else:
                break
        elif syote == "4":
            vmsyote = input(
                " 1: Luo NIC<PAKOLLINEN!>, 2: luo VM, 3: pysäytä VM, 4: käynnistä VM, 5: listaa VM:t, X: palaa: ")
            while vmsyote != "X":

                if vmsyote == "1":

                    createnic()
                    break
                elif vmsyote == "0":
                    luosubnetnic()
                    break

                elif vmsyote == "2":

                    createvm()
                    break
                elif vmsyote == "3":

                    stopvm()
                    break
                elif vmsyote == "4":

                    startvm()
                    break
                elif vmsyote == "5":
                    listvm()
                    break
        else:
            break


valitsin()
