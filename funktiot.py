from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.storage.blob import BlobClient
from azure.storage.blob import BlobServiceClient
import os
import string
import random
import datetime



now = datetime.datetime.now()

credential = AzureCliCredential()
subscription_id = os.environ["SUBSCRIPTION_ID"]
resource_client = ResourceManagementClient(credential, subscription_id)
storage_client = StorageManagementClient(credential, subscription_id)
network_client = NetworkManagementClient(credential, subscription_id)
compute_client = ComputeManagementClient(credential, subscription_id)
import parametrit

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
        parametrit.GROUP_NAME,
        {"location": "westeurope"})
    print(f"Luotiin RG nimeltä {parametrit.GROUP_NAME}")
    with open("log.txt", "a") as log:
        log.write(f"{now} luotu RG {parametrit.GROUP_NAME}")
        log.write("\n")


def getrg():
    # Get resource group
    resource_group = resource_client.resource_groups.get(
        parametrit.GROUP_NAME
    )
    print("Get resource group:\n{}".format(resource_group))


def updaterg(taginimi, tagivalue):
    # Update resource group
    resource_group = resource_client.resource_groups.update(
        parametrit.GROUP_NAME,
        {
            "tags": {
                taginimi: tagivalue,
            }
        }
    )
    print(f"Päivitettiin RG {parametrit.GROUP_NAME} tageilla {taginimi}:{tagivalue}")
    with open("log.txt", "a") as log:
        log.write(f"{now} päivitetty RG {parametrit.GROUP_NAME} tageilla {taginimi}:{tagivalue}")
        log.write("\n")



def deleterg():
    # Delete Group
    resource_client.resource_groups.begin_delete(
        parametrit.GROUP_NAME
    ).result()
    print(f"Poistettiin resource group {parametrit.GROUP_NAME}")
    with open("log.txt", "a") as log:
        log.write(f"{now} poistettu RG {parametrit.GROUP_NAME}")
        log.write("\n")


def createstorageacc():
    # Create storage account
    async_stor = storage_client.storage_accounts.begin_create(
        parametrit.GROUP_NAME,
        parametrit.STORAGE_ACCOUNT,
        {
            "sku": {
                "name": "Standard_GRS"
            },
            "kind": "StorageV2",
            "location": "westeurope",
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
    )
    async_stor.wait()
    print(f"Luotiin storage account {parametrit.STORAGE_ACCOUNT}")
    with open("log.txt", "a") as log:
        log.write(f"{now} Luotu storage account {parametrit.STORAGE_ACCOUNT}")
        log.write("\n")


def createblobcont():
    # Create blob container
    blob_container = storage_client.blob_containers.create(
        parametrit.GROUP_NAME,
        parametrit.STORAGE_ACCOUNT,
        parametrit.BLOB_CONTAINER,
        {}
    )
    print(f"Luotiin container {parametrit.BLOB_CONTAINER}")
    with open("log.txt", "a") as log:
        log.write(f"{now} luotu container {parametrit.BLOB_CONTAINER}")
        log.write("\n")


def uploadfile():
    nimi = str(input("Anna tiedoston nimi, jonka haluat uploadata: "))
    MY_CONNECTION_STRING = str(input("Anna connection string Blob containeriin: "))
    BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)
    blob = BlobClient.from_connection_string(MY_CONNECTION_STRING, parametrit.BLOB_CONTAINER, nimi)
    with open(nimi, "rb") as data:
        blob.upload_blob(data)
    print(f"Lähetetty tiedosto {nimi}")
    with open("log.txt", "a") as log:
        log.write(f"{now} lähetetty tiedosto {nimi}")
        log.write("\n")


def downloadfile():
    nimi = str(input("Anna tiedoston nimi, jonka haluat ladata: "))
    MY_CONNECTION_STRING = str(input("Anna connection string Blob containeriin: "))
    BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)
    blob = BlobClient.from_connection_string(MY_CONNECTION_STRING, parametrit.BLOB_CONTAINER, nimi)
    with open(nimi, "wb") as my_blob:
        blob_data = blob.download_blob()
        blob_data.readinto(my_blob)
    print(f"Ladattu tiedosto {nimi}")
    with open("log.txt", "a") as log:
        log.write(f"{now} ladattu tiedosto {nimi}")
        log.write("\n")


def deletefile():
    nimi = str(input("Anna tiedoston nimi, jonka haluat poistaa: "))
    MY_CONNECTION_STRING = str(input("Anna connection string Blob containeriin: "))
    BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)
    blob = BlobClient.from_connection_string(MY_CONNECTION_STRING, parametrit.BLOB_CONTAINER, nimi)
    blob.delete_blob(delete_snapshots=False)
    print(f"Poistettu tiedosto {nimi}")
    with open("log.txt", "a") as log:
        log.write(f"{now} poistettu tiedosto {nimi}")
        log.write("\n")


def deletecontainer():
    blob_container = storage_client.blob_containers.delete(
        parametrit.GROUP_NAME,
        parametrit.STORAGE_ACCOUNT,
        parametrit.BLOB_CONTAINER
    )
    print(f"Poistettiin container {parametrit.BLOB_CONTAINER}")
    with open("log.txt", "a") as log:
        log.write(f"{now} poistettu container {parametrit.BLOB_CONTAINER}")
        log.write("\n")


def listvnet():
    result_create = network_client.virtual_networks.list(
        parametrit.GROUP_NAME,
    )
    for re in result_create:
        print(re.name)


def createvnet(nimi="defaultvnet"):
    # Create virtual network
    network = network_client.virtual_networks.begin_create_or_update(
        parametrit.GROUP_NAME,
        parametrit.VIRTUAL_NETWORK_NAME,
        {
            "address_space": {
                "address_prefixes": [
                    "10.0.0.0/16"
                ]
            },
            "location": "westeurope"
        }
    ).result()
    print(f"Luotiin VNET {parametrit.VIRTUAL_NETWORK_NAME}")
    with open("log.txt", "a") as log:
        log.write(f"{now} luotu VNET {parametrit.VIRTUAL_NETWORK_NAME}")
        log.write("\n")


def createsubnet(subnetCIDR):
    # Create subnet
    subnet = network_client.subnets.begin_create_or_update(
        parametrit.GROUP_NAME,
        parametrit.VIRTUAL_NETWORK_NAME,
        parametrit.SUBNET_NAME,
        {
            "address_prefix": subnetCIDR
        }
    ).result()
    print(f"Luotiin subnet {parametrit.SUBNET_NAME}")
    with open("log.txt", "a") as log:
        log.write(f"{now} luotu subnet {parametrit.SUBNET_NAME}")
        log.write("\n")


def deletesubnet():
    # Delete subnet
    subnet = network_client.subnets.begin_delete(
        parametrit.GROUP_NAME,
        parametrit.VIRTUAL_NETWORK_NAME,
        parametrit.SUBNET_NAME
    ).result()
    print(f"Poistettiin subnet {parametrit.SUBNET_NAME}")
    with open("log.txt", "a") as log:
        log.write(f"{now} poistettu subnet {parametrit.SUBNET_NAME}")
        log.write("\n")


def deletevnet():
    network = network_client.virtual_networks.begin_create_or_update(
        parametrit.GROUP_NAME,
        parametrit.VIRTUAL_NETWORK_NAME)
    print(f"Poistetu VNET {parametrit.VIRTUAL_NETWORK_NAME}")
    with open("log.txt", "a") as log:
        log.write(f"{now} poistettu VNET {parametrit.VIRTUAL_NETWORK_NAME}")
        log.write("\n")


def luosubnetnic():
    async_subnet = network_client.subnets.begin_create_or_update(
        parametrit.GROUP_NAME,
        parametrit.NETWORK_NAME,
        parametrit.NICSUBNET,
        {'address_prefix': '10.1.0.0/24'}
    )
    async_subnet.wait()
    print(f"Luotiin Subnet {parametrit.NICSUBNET}")



def createnic():
    # Create network interface
    network_client.network_interfaces.begin_create_or_update(
        parametrit.GROUP_NAME,
        parametrit.INTERFACE_NAME,
        {
            'location': "westeurope",
            'ip_configurations': [{
                'name': 'MyIpConfig',
                'subnet': {
                    'id': str(
                        f"/subscriptions/{subscription_id}/resourceGroups/{parametrit.GROUP_NAME}/providers/Microsoft.Network/virtualNetworks/{parametrit.VIRTUAL_NETWORK_NAME}/subnets/{parametrit.SUBNET_NAME}")
                }
            }]
        }
    ).result()


def createvm():
    NICNIMI = "nic" + ''.join(random.choice(string.ascii_lowercase) for u in range(8))
    network_client.network_interfaces.begin_create_or_update(
        parametrit.GROUP_NAME,
        NICNIMI,
        {
            'location': "westeurope",
            'ip_configurations': [{
                'name': 'MyIpConfig',
                'subnet': {
                    'id': str(
                        f"/subscriptions/{subscription_id}/resourceGroups/{parametrit.GROUP_NAME}/providers/Microsoft.Network/virtualNetworks/{parametrit.VIRTUAL_NETWORK_NAME}/subnets/{parametrit.SUBNET_NAME}")
                }
            }]
        }
    ).result()
    with open("log.txt", "a") as log:
        log.write(f"{now} luotu NIC {NICNIMI}")
        log.write("\n")

    vm = compute_client.virtual_machines.begin_create_or_update(
        parametrit.GROUP_NAME,
        parametrit.VM_NAME,
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
                    "name": parametrit.OS_DISK,
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
                "admin_password": parametrit.your_password,
                "windows_configuration": {
                    "enable_automatic_updates": True  # need automatic update for reimage
                }
            },
            "network_profile": {
                "network_interfaces": [
                    {
                        "id": "/subscriptions/" + subscription_id + "/resourceGroups/" + parametrit.GROUP_NAME + "/providers/Microsoft.Network/networkInterfaces/" + NICNIMI + "",
                        # "id": NIC_ID,
                        "properties": {
                            "primary": True
                        }
                    }
                ]
            }
        }
    ).result()
    print(f"Luotiin VM nimeltä {parametrit.VM_NAME}")
    with open("log.txt", "a") as log:
        log.write(f"{now} luotu VM {parametrit.VM_NAME}")
        log.write("\n")


def stopvm(nimi=parametrit.VM_NAME):
    # Stop the VM
    print('"\n"Pysäytetään VM')
    async_vm_stop = compute_client.virtual_machines.begin_power_off(
        parametrit.GROUP_NAME, nimi)
    async_vm_stop.wait()
    with open("log.txt", "a") as log:
        log.write(f"{now} pysäytetty VM {nimi}")
        log.write("\n")


def startvm(nimi=parametrit.VM_NAME):
    # Start the VM
    print('"\n"Käynnistetään VM')
    async_vm_start = compute_client.virtual_machines.begin_start(
        parametrit.GROUP_NAME, nimi)
    async_vm_start.wait()
    with open("log.txt", "a") as log:
        log.write(f"{now} käynnistetty VM {nimi}")
        log.write("\n")


def listvm():
    result_create = compute_client.virtual_machines.list(
        parametrit.GROUP_NAME,
    )
    for re in result_create:
        print(re.name)

