import pyodbc, logging, os, uuid, sys, csv, shutil, json
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from datetime import datetime
from shutil import copy
import numpy as np

#-----------Log file-----------#
logging.basicConfig(filename=datetime.now().strftime(os.path.abspath(r"./Logs/createProject_%H_%M_%S_%d_%m_%Y.log")), level=logging.INFO)

#-----------Project Name-------------#
#The project name will be the same for csvfile and Azure container, then avoid using spaces or special characteres.

#Menu functions
def inputNumber(prompt):
    while True:
        try:
            num = float(input(prompt))
            break
        except ValueError:
            pass

    return num

def displayMenu(options):
    for i in range(len(options)):
        print("\n","{:d}. {:s}".format(i+1, options[i]))

    choice = 0
    while not(np.any(choice == np.arange(len(options))+1)):
        choice = inputNumber("\nPlease choose a menu item: ")

    return choice

#Create Menu
menuItems = np.array(["Enter Project Name(Same name VIEW Sql Server, without prefix v_)","Display Project Name","Create Folders Structure and CSV File\n"])
project = "Unnamed Project"

while True:
    
    choice = displayMenu(menuItems)

    if choice == 1:
        viewName = input("\nPlease enter Project Name: ")
        project = viewName.replace("_","-")
        path = os.chdir(r"../Projects")
        projects = os.listdir(path)
        for i in projects:
            if(i == project):
                print("\nIt already have a project with this name! Pich another one\n")
    elif choice == 2:
        print("\nProject Name: "+project+"\n")

    elif choice == 3:
        break

#-----------Folders Structure-------------#
os.chdir(r"../Projects")
os.mkdir(project)
os.chdir(project)
os.mkdir("Files")
os.mkdir("Scripts")
os.mkdir("Logs")

#-----------Csv File-------------#

os.chdir("Files")
with open(project+".csv", "w") as my_empty_csv:
  pass

src = (os.path.abspath(r"../../../Scripts/FromSqlServer-ToCsv-ToAzure.py"))
dst = (os.path.abspath(r"../Scripts/"))
shutil.copy(src, dst, follow_symlinks=True)

#-----------Azure Container-------------#

blob_service = BlobServiceClient(account_url="storage blob url", account_name='storage account name', account_key='storage account key with write permissions')

#Create Menu
menuItems = np.array(["Create Container in Azure", "List Containers in Azure", "Quit"])

while True:
    
    choice = displayMenu(menuItems)

    if choice == 1:
        container = blob_service.create_container(project)

    elif choice == 2:
        containers = blob_service.list_containers()
        print("\n")
        for c in containers: 
            print(c.name)

    elif choice == 3:
        break

containerUrl = 'https://'+blob_service.account_name+'.dfs.core.windows.net/'+project; #This URL will be used to connect in container by Power BI.

print("\n---------Project Summary-----------\n")
print("Project Name: "+project)
print("CSV File: "+project+".csv")

containers = blob_service.list_containers()
for c in containers:
    if(c.name == project):
        print("Azure Container Name: "+project)
        print("Azure Container URL: "+containerUrl)
            
logging.info("\n---------Project Summary-----------\n")
logging.info("Project Name: "+project)
logging.info("CSV File: "+project+".csv")
logging.info("Azure Container Name: "+project)
logging.info("Azure Container URL: "+containerUrl)

















