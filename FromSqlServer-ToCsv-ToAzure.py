import pyodbc, logging, os, uuid, sys, csv
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from datetime import datetime

#-----------Log file-----------#
logging.basicConfig(filename=datetime.now().strftime(os.path.abspath(r"../Logs/databaseExtract_%H_%M_%S_%d_%m_%Y.log")), level=logging.INFO)

#--------Connection and statement execution--------#

#create the connection
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=serverName;PORT=1433;DATABASE=database;UID=user;PWD=pass') 
#create the cursor
cursor = conn.cursor()
#Execute the statement
csvfile = os.listdir(os.path.abspath(r"../Files/")) #pegando o nome do projeto
project = os.path.splitext(csvfile[0])[0]

string = statement = ("SELECT * FROM v_"+project) #rename name-of-view to name_of_view / sql server doesn't permit - char in statement
statement = string.replace("-", "_")
cursor.execute(statement)

try:
    cursor.execute(statement)
    rows = cursor.fetchall()
finally:
    conn.close()

#-----------Export to csv-------------#

try:  
    local_path=(os.path.abspath(r"../Files/"))
    csvfile = os.listdir(local_path)
    local_file_name = "\\"+csvfile[0]
    full_path_to_file = (local_path+local_file_name)

    # New empty list called 'result'. This will be written to a file.
    result = list()

    # The row name is the first entry for each entity in the description tuple.
    column_names = list()
    for i in cursor.description:
        column_names.append(i[0])

    result.append(column_names)
    for row in rows:
        result.append(row)

    # Write result to file.
    with open(full_path_to_file, 'w', newline='') as file:
        csvwriter = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in result:
            csvwriter.writerow(row)

    logging.info("Criação do Arquivo CSV - OK")
except:
    logging.info("Criação do Arquivo CSV - ERROR")

#--------Upload Files to Azure--------#

try:
    #Azure Connection
    blob_service = BlobServiceClient(account_url="your azure account url here", account_name='storage account name', account_key='storage account key with write permissions')

    #container recebe o mesmo nome do arquivo csv
    filename = os.path.basename(local_file_name)
    container_name = os.path.splitext(filename)[0]
    
    logging.info("Conexão com Azure - OK")
except:
    logging.info("Conexão com Azure - ERROR")
    
try:
    #Local File
    local_path=(os.path.abspath(r"../Files/"))
    csvfile = os.listdir(local_path)
    local_file_name = "/"+csvfile[0]
    full_path_to_file = (local_path+local_file_name)
    
    logging.info("Arquivo Local - OK")
except:
    logging.info("Arquivo Local - ERROR")
    
try:
    #Upload Local File to Container
    blob_client = blob_service.get_blob_client(container=container_name, blob=local_file_name)
    with open(full_path_to_file, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    
    logging.info("Upload do CSV para o Azure - OK")
except:
    logging.info("Upload do CSV para o Azure - ERROR")
