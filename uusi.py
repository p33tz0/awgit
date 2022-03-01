import argparse
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

parser = argparse.ArgumentParser()
args = parser.parse_args()

GROUP_NAME = "PetrusRG"
STORAGE_ACCOUNT = "petrusstorage"
BLOB_CONTAINER = "petrusblob"
VIRTUAL_NETWORK_NAME = "petrusvnet"
blob_name = BLOB_CONTAINER
MY_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=petrusstorage;AccountKey=iHmo4BRf5tzNaf7iPWDCTdIPwj6+azg/2J9Xg1nZuEyVz60GeAqeB22SEZ9hLeEC+I399bI66nsN+AStiDmHQQ==;EndpointSuffix=core.windows.net"
SUBNET_NAME = "petrussubnet"
INTERFACE_NAME = "petrusinterface"
NETWORK_NAME = "petrusvnet"
VIRTUAL_MACHINE_EXTENSION_NAME = "petrusextension"
your_password = 'A1_' + ''.join(random.choice(string.ascii_lowercase) for i in range(8))

credential = AzureCliCredential()
subscription_id = os.environ["SUBSCRIPTION_ID"]
resource_client = ResourceManagementClient(credential, subscription_id)
storage_client = StorageManagementClient(credential, subscription_id)
network_client = NetworkManagementClient(credential, subscription_id)
compute_client = ComputeManagementClient(credential, subscription_id)
BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)


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


def updaterg():
    # Update resource group
    resource_group = resource_client.resource_groups.update(
        GROUP_NAME,
        {
            "tags": {
                "name": "value",
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


def uploadfile(nimi):
    blob = BlobClient.from_connection_string(MY_CONNECTION_STRING, BLOB_CONTAINER, nimi)
    with open(nimi, "rb") as data:
        blob.upload_blob(data)


def downloadfile(nimi):
    blob = BlobClient.from_connection_string(MY_CONNECTION_STRING, BLOB_CONTAINER, nimi)
    with open(nimi, "wb") as my_blob:
        blob_data = blob.download_blob()
        blob_data.readinto(my_blob)


def deletefile(nimi):
    blob = BlobClient.from_connection_string(MY_CONNECTION_STRING, BLOB_CONTAINER, nimi)
    blob.delete_blob(delete_snapshots=False)


def deletecontainer():
    blob_container = storage_client.blob_containers.delete(
        GROUP_NAME,
        STORAGE_ACCOUNT,
        BLOB_CONTAINER
    )
    print("Delete blob container.\n")


def listvnet():
    result_create = network_client.virtual_networks.list(
        GROUP_NAME,
    )
    for re in result_create:
        print(re.name)


def createvnet(nimi):
    # Create virtual network
    network = network_client.virtual_networks.begin_create_or_update(
        GROUP_NAME,
        nimi,
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


def createsubnet(vnetName, subnetName, subnetCIDR):
    # Create subnet
    subnet = network_client.subnets.begin_create_or_update(
        GROUP_NAME,
        vnetName,
        subnetName,
        {
            "address_prefix": subnetCIDR
        }
    ).result()
    print("Create subnet:\n{}".format(subnet))


def deletesubnet(nimi):
    # Delete subnet
    subnet = network_client.subnets.begin_delete(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME,
        nimi
    ).result()
    print("Delete subnet.\n")


def deletevnet(nimi):
    network = network_client.virtual_networks.begin_create_or_update(
        GROUP_NAME,
        nimi)


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
                    'id': "/subscriptions/397dc614-480f-46f5-a35f-d4e5d10d1095/resourceGroups/PetrusRG/providers/Microsoft.Network/virtualNetworks/petrusvnet/subnets/petrussubnet"
                }
            }]
        }
    ).result()


def createvm(nimi):
    vm = compute_client.virtual_machines.begin_create_or_update(
        GROUP_NAME,
        nimi,
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
                    "name": "myVMosdisk",
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
                        "id": "/subscriptions/" + subscription_id + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/networkInterfaces/" + INTERFACE_NAME + "",
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


def stopvm(nimi):
    # Stop the VM
    print('\nStop VM')
    async_vm_stop = compute_client.virtual_machines.begin_power_off(
        GROUP_NAME, nimi)
    async_vm_stop.wait()


def startvm(nimi):
    # Start the VM
    print('\nStart VM')
    async_vm_start = compute_client.virtual_machines.begin_start(
        GROUP_NAME, nimi)
    async_vm_start.wait()


def listvm():
    result_create = compute_client.virtual_machines.list(
        GROUP_NAME,
    )
    for re in result_create:
        print(re.name)


listvm()
