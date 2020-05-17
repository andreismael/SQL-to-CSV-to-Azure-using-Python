# SQL-to-CSV-to-Azure-using-Python
Extract data from SQL Server, input in a CSV file, and upload the file to Azure to be consumed by Power BI.

# Requirements
* Python 3.7.6
  * Libs: pyodbc, shutil, azure.storage.blob, numpy.
* Azure Storage account type: Data Lake Storage Gen2.
* SQL Server 2014.
* Host with Win Server or Win 10 installed.

# Implementing the Project Step by Step

## SQL Server:
* Create a view and name it like "v_name_of_view".

![viewSql](https://github.com/andreismael/SQLServer-to-CSV-to-AzureBlobStorage-using-Python/blob/master/Images/viewSqlServer.png)
  
## Azure Portal:
1. Create a new storage account of type "Data Lake Storage Gen2".

![createStorageAccount](https://github.com/andreismael/SQLServer-to-CSV-to-AzureBlobStorage-using-Python/blob/master/Images/storageAccountAzure.png)

2. Create a new SAS(Shared Access Signature) with write permissions.

![sasAzure](https://github.com/andreismael/SQLServer-to-CSV-to-AzureBlobStorage-using-Python/blob/master/Images/sasAzure.png)

3. Copy the "Blob service SAS URL", "Storage Account Name" and the "Access Key".

![storageAccountURL](https://github.com/andreismael/SQLServer-to-CSV-to-AzureBlobStorage-using-Python/blob/master/Images/blobServiceSasURL.png)

![accessKey](https://github.com/andreismael/SQLServer-to-CSV-to-AzureBlobStorage-using-Python/blob/master/Images/accessKey.png)

## Host Settings:
1. Install Python 3.7.6 - https://www.python.org/downloads/release/python-376/.

![pythonInstall](https://github.com/andreismael/SQLServer-to-CSV-to-AzureBlobStorage-using-Python/blob/master/Images/pythonInstall.png)

2. Install Libs(pyodbc, shutil, azure.storage.blob, numpy) with pip, example: "pip install pyodbc".

![pipInstall](https://github.com/andreismael/SQLServer-to-CSV-to-AzureBlobStorage-using-Python/blob/master/Images/pipInstall.png)

3. Create the follow folder structure where you want to store your projects:

![structureFolders](https://github.com/andreismael/SQLServer-to-CSV-to-AzureBlobStorage-using-Python/blob/master/Images/structureFolders.png)

4. Put both scripts in "Scripts" Folder(CreateNewProject.py, FromSqlServer-ToCsv-ToAzure.py).
5. Edit the script CreateNewProject.py. Replace "account_url" to your "Blob service SAS URL", "account_name" to the name of the Storage Account, and "access_key" to your access_key, copied in the second step of **"In Azure Portal"**.

![replaceScriptCreateProject](https://github.com/andreismael/SQLServer-to-CSV-to-AzureBlobStorage-using-Python/blob/master/Images/replaceScriptCreateProject.png)

6. Edit the script FromSqlServer-ToCsv-ToAzure.py. Replace the SQL Server connection info(where your view are stored) and Azure Connection(account_name, account_url and access_key).

![replaceSqlServerInfoScript](https://github.com/andreismael/SQLServer-to-CSV-to-AzureBlobStorage-using-Python/blob/master/Images/replaceSqlServerInfoScript.png)

![replaceAzureConnectionInfoScript](https://github.com/andreismael/SQLServer-to-CSV-to-AzureBlobStorage-using-Python/blob/master/Images/replaceAzureConnectionInfoScript.png)

7. Run "CreateNewProject.py". 
    - Press 1 to input the project name(*same name of view, without prefix v_*);
    - Press 2 if you want to see the project name;
    - Press 3 if you want to create a description for the project;
    - Press 4 to create the structure folder of the project;
    - After, Press 1 to create the container in Azure and 3 to quit.
8. Consult logs in Analytics/Scripts/Logs and copy the "Azure Container URL". *You will need this for the PowerBI steps*.

![containerURL](https://github.com/andreismael/SQLServer-to-CSV-to-AzureBlobStorage-using-Python/blob/master/Images/containerURL.png)

9. Access folder "Analytics/Projects/Your Project/Scripts".
10. Execute "FromSqlServer-ToCsv-ToAzure.py".
11. Check the log in "Analytics/Projects/Your Project/Logs". 
12. Check the CSV File in "Analytics/Projects/Your Project/Files" and in the Azure Container.

## Scheduling Script in Windows:
1. Get directory where Python is installed.

![dirPython](https://github.com/andreismael/SQLServer-to-CSV-to-AzureBlobStorage-using-Python/blob/master/Images/dirPython.png)

2. Open the Windows Task Scheduler.
3. Create a new task.
4. Configure the Triggers.
5. Configure the Action like below:

![taskSchd](https://github.com/andreismael/SQLServer-to-CSV-to-AzureBlobStorage-using-Python/blob/master/Images/taskSchd.png)
  
## Container Permission in Azure Portal:
* Option 1- If you have Azure AD, you can add the "Storage Blog Data Reader" for a user in Access Control of the container.

![roleStorageBlobDataReader](https://github.com/andreismael/SQLServer-to-CSV-to-AzureBlobStorage-using-Python/blob/master/Images/roleStorageBlobDataReader.png)

* Option 2- Create a SAS(Shared Access Signature) in the container, to users access data(csv) in PowerBI using Access Key.
  
## Getting Data by PowerBI:
1. Get Data - Azure - Azure Data Lake Storage Gen2.

![powerbiStorageGen2](https://github.com/andreismael/SQLServer-to-CSV-to-AzureBlobStorage-using-Python/blob/master/Images/powerbiStorageGen2.png)

2. URL: Get the container URL in Analytics/Scripts/Logs/create_project..txt. Ex: https://storageaccount.dfs.core.windows.net/container.

![containerURL](https://github.com/andreismael/SQLServer-to-CSV-to-AzureBlobStorage-using-Python/blob/master/Images/containerURL.png)

![URLStorageGen2](https://github.com/andreismael/SQLServer-to-CSV-to-AzureBlobStorage-using-Python/blob/master/Images/URLStorageGen2.png)

3. If you implemented Option 1 in "Container Permission Settings in Azure Portal" step, then choose "Organization Account" and login with your Azure AD Account. 

![orgAccountPowerBI](https://github.com/andreismael/SQLServer-to-CSV-to-AzureBlobStorage-using-Python/blob/master/Images/orgAccountPowerBI.png)

4. If you implemented Option 2 in "Container Permission Settings in Azure Portal" step, then choose "Account Key" and paste the "container account key".
  
![accountKeyPowerBI](https://github.com/andreismael/SQLServer-to-CSV-to-AzureBlobStorage-using-Python/blob/master/Images/accountKeyPowerBI.png)
  
