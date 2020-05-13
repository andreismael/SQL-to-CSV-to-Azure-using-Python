# SQLServer-to-CSV-to-AzureBlobStorage-using-Python
Extract data from SQL Server, input in a CSV file, and upload the file to Azure to be consumed by Power BI.

# Requirements
* Python 3.7.6
  * Libs: pyodbc, shutil, azure.storage.blob, numpy.
* Azure Storage account type: Data Lake Storage Gen2.
* SQL Server 2014.
* Host with Win Server or Win 10 installed.

# Implement project step by step

## In SQL Server:
* Create a view and name it like "v_name_of_view".
  
## In Azure Portal:
1. Create a new storage account of type "Data Lake Storage Gen2".
2. Create a new SAS(Shared Access Signature) with write permissions and copy the "Blob service SAS URL", "Storage Account Name" and the "Access Key".

## In the Host:
1. Install Python 3.7.6 - https://www.python.org/downloads/release/python-376/.
2. Install Libs with pip, example: "pip install pyodbc".
3. Create the follow folder structure where you want to store your projects:
  * Analytics
    * Projects
    * Scripts
      * Logs
4. Put both scripts in "Scripts" Folder(CreateNewProject.py, FromSqlServer-ToCsv-ToAzure.py).
5. Edit the script CreateNewProject.py. Replace "account_url" to your "Blob service SAS URL", "account_name" to the name of the Storage Account, and "access_key" to your access_key, copied in the second step of **"In Azure Portal"**.
6. Edit the script FromSqlServer-ToCsv-ToAzure.py. Replace the SQL Server connection info(where your view are stored) and Azure Connection(account_name, account_url and access_key).
7. Run CreateNewProject.py. Press 1 to input the project name(*same of view name, without prefix v_*) and press 3 to create the structure folder of the project. After that, press 1 to create the container in Azure.
8. Consult logs in Analytics/Scripts/Logs and copy the "Azure Container URL". You will need this for the PowerBI steps.
9. Access folder Analytics/Projects/Your Project/Scripts.
10. Execute FromSqlServer-ToCsv-ToAzure.py.
11. Check the log in Analytics/Projects/Your Project/Logs and the CSV File in Analytics/Projects/Your Project/Files and in Azure Container.
  
## Container Permission Settings in Azure Portal:
* Option 1- If you have Azure AD, you can add the "Storage Blog Data Reader" for a user in Access Control of the container.
* Option 2- You can create a SAS(Shared Access Signature) for the users access data(csv) in PowerBI using Access Key.
  
## In PowerBI:
1. Get Data - Azure - Azure Data Lake Storage Gen2.
2. URL: Get the container URL in Analytics/Scripts/Logs/create_project..txt. Ex: https://storageaccount.dfs.core.windows.net/container.
3. Choose "Organization Account" and login with your Azure AD Account if you implemented Option 1 in "Container Permission Settings in Azure Portal" step.
4. Choose "Account Key" and paste the "container account key" if you implemented Option 2 in "Container Permission Settings in Azure Portal" step.
  

  
