# eagle module for Rover deployment
# code snippets needed for Rover are in this module
##################################################################################################
from azure.cli.core import get_default_cli
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.storage.blob import ContainerClient
import os

# Acquire a credential object.
credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)

def az_cli (args_str):
    args = args_str.split()
    print(args)
    cli = get_default_cli()
    cli.invoke(args)
    print(cli.result.result)
    if cli.result.result:
        return cli.result.result
    elif cli.result.error:
        raise cli.result.error
    return True

def main():

	# Retrieve subscription ID from azure.
	subscription_id = az_cli("account show --query id --output tsv")
	subscription_id = az_cli( " account set --subscription " + "DSG_NA_DEVTEST_1")
	
	#get spaform file for data
	####################################################
	### config File Read
	####################################################
	from configparser import ConfigParser 
	
	initmp = "dsgtmp.ini"
	configur = ConfigParser() 
	ini_file = os.path.join(os.path.dirname(__file__)+ "/" , initmp)
	
	rcfg = configur.read(ini_file)
	nam = (configur.get('install', 'CLI_NME')) 
	wst = (configur.get('install', 'wurl'))
	acr = (configur.get('install', 'acronym'))
	file_path = (configur.get('install', 'work_path')) 
	configur.remove_section('install')
	###############################################################
	
	#location selection
	#loc = az_cli[" account list-locations --output json | jq '.[] | select(.displayName == "UAE North") | { "code": .name }'"]
	
	LOCATION = "east us"
	
	###############################################################
	
	# create our resource group
	GROUP_NAME = "DSG_NA_DEVTEST_RESOURCES"
	
	#response = az_cli("group create -n  " + GROUP_NAME + " -l" + LOCATION)
	###############################################################
	# create a storage account
	STORAGE_ACCOUNT_NAME = "dsgnadevteststor"
	#az storage account create -n $storageAccount -g $resourceGroup -l $location --sku Standard_LRS
	###############################################################
	#### storage account key
	response = az_cli(" storage account keys list -n  "+ STORAGE_ACCOUNT_NAME + " -g " + GROUP_NAME +" --query [0].value -o tsv")
	sak = response
	###############################################################
	#container for client
	containerName = "dsgix"+acr+"cont"
	response = az_cli(" storage container create --name " + containerName + "  --account-name " + STORAGE_ACCOUNT_NAME + " --auth-mode login")
	#print(response)
	###############################################################
	## connect string
	cs = az_cli(" storage account show-connection-string -n "+ STORAGE_ACCOUNT_NAME + "  -g " + GROUP_NAME +"  --query connectionString -o tsv")
	#print(cs)
	################################################################################
	#eventhub namespace is supplied for SMB and Growth customers
	#we need to add eventhub and sas policy
	
	'''
	#fom azhelper import az_cli
	#print(GROUP_NAME)
	ehnam = az_cli("eventhubs namespace create --resource-group " + GROUP_NAME + " --name " + NAMESPACE_NAME + " --location " + LOCATION + " --tags tag1=v1 tag2=v2 --sku Standard --enable-auto-inflate --maximum-throughput-units 20")
	#print("%s" % (response))
	'''
	NAMESPACE_NAME = "dsgehns1"
	
	###############################################
	#eventhub create
	
	EVENTHUB_NAME = "dsgix_"+acr+"_eh"
	
	resp = az_cli("eventhubs eventhub create --name " + EVENTHUB_NAME + "  --namespace-name " + NAMESPACE_NAME + " --resource-group " + GROUP_NAME + " --blob-container " + containerName +" --enable-capture true --mi-system-assigned true --capture-interval 300  --cleanup-policy Delete  --partition-count 4 --retention-time 120 --skip-empty-archives true --status Active --storage-account " + STORAGE_ACCOUNT_NAME + " --destination-name EventHubArchive.AzureBlockBlob")
	#print("%s" % (response)
	
	pname=EVENTHUB_NAME+"_sas"
	#authorization rule - SAS policy create
	response = az_cli(" eventhubs eventhub authorization-rule create --resource-group "+ GROUP_NAME + " --namespace-name " + NAMESPACE_NAME + " --eventhub-name " + EVENTHUB_NAME + " --name " + pname + " --rights Listen Send ")
	#print("%s" % (response))
	
	auth = az_cli( " eventhubs eventhub authorization-rule create --resource-group "+ GROUP_NAME + " --namespace-name " + NAMESPACE_NAME +" --eventhub-name "+ EVENTHUB_NAME +" --name " + pname +" --rights Manage Listen Send ")

	# eventhub connect string extract
	ehcs = "Endpoint=sb://dsgehns1.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=Jh45BPMHxGD71gFLYCwEUbHftoq4dIMlj+AEhA6/4w8="
	#print(ehcs)
	###############################################################
	
	filnam = os.path.join(os.path.dirname(__file__)+"/","dsgix"+acr+".ini")
	savfil = os.path.join(os.path.dirname(__file__)+"/","dsgfile.txt")
	configur.remove_section('install')
	configur.add_section('installation')
	 
	sanm= STORAGE_ACCOUNT_NAME
	cn = "dsgix-"+acr+"-cont"
	ehnam=EVENTHUB_NAME
	wp= "/"
	
	configur.set('installation', 'CLI_NME',nam)
	configur.set('installation', 'wurl',wst)
	configur.set('installation', 'acronym',acr)
	configur.set('installation', 'storage_account_key',sak)
	configur.set('installation', 'storage_account_name',sanm)
	configur.set('installation', 'connection_string',cs)
	configur.set('installation', 'container_name',cn)
	configur.set('installation', 'eventhub_name',ehnam)
	configur.set('installation', 'eh_connection_string',ehcs)
	#configur.set('Installation','puv_month',pu)
	configur.set('installation', 'work_path',wp)
	
	 # save to a file
	with open(filnam, 'w') as configfile:
	 configur.write(configfile)
	#print('0: '+ filnam)
	with open(savfil, 'w') as gfile:
	 gfile.write(filnam)
	return 1


if __name__ == "__main__":
    main()
