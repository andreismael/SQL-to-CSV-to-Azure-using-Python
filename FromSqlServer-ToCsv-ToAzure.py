import pyodbc, logging, os, uuid, sys, csv
from datetime import datetime
from azure.storage.blob import BlobServiceClient

#-----------Log file-----------#
logging.basicConfig(filename=datetime.now().strftime(os.path.abspath(r"../Logs/databaseExtract_%H_%M_%S_%d_%m_%Y.log")), level=logging.INFO)
logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(logging.WARNING) #disable policy logs from azure

#--------Connection and statement execution--------#

#create the connection
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=SQL Server;PORT=1433;DATABASE=database;UID=user;PWD=pass') 
#create the cursor
cursor = conn.cursor()
#Execute the statement
csvfile = os.listdir(os.path.abspath(r"../Files/")) #pegando o nome do projeto
project = os.path.splitext(csvfile[0])[0]
logging.info(datetime.now().strftime("Time:%H:%M:%S-Query SQL-Running"))
string = statement = ("SELECT * FROM v_"+project) #rename name-of-view to name_of_view / sql server doesn't permit - char in statement
statement = string.replace("-", "_")
cursor.execute(statement)
#Get columns
columns = [column[0] for column in cursor.description]
#Get results
row = cursor.fetchone()
logging.info(datetime.now().strftime("Time:%H:%M:%S-Query SQL-Finished"))

#-----------Export to csv-------------#
logging.info(datetime.now().strftime("Time:%H:%M:%S-CSV File-Writing"))
local_path=(os.path.abspath(r"../Files/"))
csvfile = os.listdir(local_path)
local_file_name = "\\"+csvfile[0]
full_path_to_file = (local_path+local_file_name)

with open(full_path_to_file,"w",newline='', encoding='utf-8-sig') as file:
    csvwriter = csv.writer(file, delimiter='|')
    csvwriter.writerow(columns)
    while row:
       csvwriter.writerow(row)
       row = cursor.fetchone()
 
#Close cursor
cursor.close()  
#Close connection
conn.close()
logging.info(datetime.now().strftime("Time:%H:%M:%S-CSV File-Finished"))
#--------Upload Files to Azure--------#

try:
    #Azure Connection
    blob_service = BlobServiceClient(account_url="your account URL", account_name='storage account name', account_key='account key')

    #container recebe o mesmo nome do arquivo csv
    filename = os.path.basename(local_file_name)
    container_name = os.path.splitext(filename)[0]
    
    logging.info(datetime.now().strftime("Time:%H:%M:%S-Azure Connection - OK"))
except:
    logging.info(datetime.now().strftime("Time:%H:%M:%S-Azure Connection - FAILED"))
    
try:
    #Local File
    local_path=(os.path.abspath(r"../Files/"))
    csvfile = os.listdir(local_path)
    local_file_name = "/"+csvfile[0]
    full_path_to_file = (local_path+local_file_name)
    
    logging.info(datetime.now().strftime("Time:%H:%M:%S-Local File - OK"))
except:
    logging.info(datetime.now().strftime("Time:%H:%M:%S-Local File - ERROR"))
    
try:
    #Upload Local File to Container
    logging.info(datetime.now().strftime("Time:%H:%M:%S-CSV to Azure-Uploading"))
    blob_client = blob_service.get_blob_client(container=container_name, blob=local_file_name)
    with open(full_path_to_file, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    
    logging.info(datetime.now().strftime("Time:%H:%M:%S-CSV to Azure-Finished"))
except:
    logging.info(datetime.now().strftime("Time:%H:%M:%S-Upload CSV to Azure - FAILED"))

