import pyodbc, logging, os, uuid, sys, csv, shutil, json
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from datetime import datetime
from shutil import copy
import numpy as np

logsCreateProject = "C:/TI Analytics/Scripts/Logs"
projectsDir = "C:/TI Analytics/Projects"

#-----------Project Name-------------#
#O nome do projeto será usado para criar o arquivo csv local e também o container no Azure,
#por isso nao poderá ter espaços ou caracteres especiais.

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
menuItems = np.array(["Enter Project Name(Same name VIEW Sql Server, without prefix v_)","Display Project Name","Enter Project Description","Create Folders Structure and CSV File\n"])
project = "Unnamed Project"

while True:
    
    choice = displayMenu(menuItems)

    if choice == 1:
        viewName = input("\nPlease enter Project Name: ")
        project = viewName.replace("_","-")
        path = os.chdir(projectsDir)
        projects = os.listdir(path)
        for i in projects:
            if(i == project):
                print("\nIt already have a project with this name! Pich another one\n")
    elif choice == 2:
        print("\nProject Name: "+project+"\n")

    elif choice == 3:
        requester = input("\nRequester: ")
        objective = input("\nObjective: ")
        requestDate = input("\nRequest Date: ")
        with open("readme_"+project+".txt", "w") as file:
            file.write("Requester: "+requester+"\n")
            file.write("Objective: "+objective+"\n")
            file.write("Request Date: "+requestDate+"\n")
            file.close

    elif choice == 4:
        break

#-----------Folders Structure-------------#
os.chdir(projectsDir)
os.mkdir(project)
os.chdir(project)
if os.path.exists(os.path.abspath(r"../readme_"+project+".txt")):
    src = (os.path.abspath(r"../readme_"+project+".txt"))
    dst = (os.path.abspath(r"./"))
    shutil.move(src, dst)
else:
    print("Readme does not exists!")
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

blob_service = BlobServiceClient(account_url="your account URL", account_name='storage account name', account_key='account key')

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

containerUrl = 'https://'+blob_service.account_name+'.dfs.core.windows.net/'+project;

print("\n---------Project Summary-----------\n")
print("Project Name: "+project)
print("CSV File: "+project+".csv")

containers = blob_service.list_containers()
for c in containers:
    if(c.name == project):
        print("Azure Container Name: "+project)
        print("Azure Container URL: "+containerUrl)

#-----------Log file-----------#
logging.basicConfig(filename=datetime.now().strftime(os.path.abspath(r"C:/TI Analytics/Scripts/Logs/createProject_"+project+"_%H_%M_%S_%d_%m_%Y.log")), level=logging.INFO)

logging.info("\n---------Project Summary-----------\n")
logging.info("Project Name: "+project)
logging.info("CSV File: "+project+".csv")
logging.info("Azure Container Name: "+project)
logging.info("Azure Container URL: "+containerUrl)

















