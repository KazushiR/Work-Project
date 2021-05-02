import sys
sys.path.append(r"C:\Users\Name\Desktop\PythonProjects\Company PI\Company State Locations")
from Server_Locations import Tokien_ID
import csv, os, requests

os.chdir(r"C:\Users\Name\Desktop\PythonProjects\Company API\Company Server List")

#inputs the server that is having the issue
Server_number = input("What server is having issues? ")
ServerURL = f"SErver URL"

headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {Tokien_ID}'
    ,
}
#list of server numbers and sets it as a list ID
company_dictionary = {20: "ID", 22: "ID", 23: "ID", 24: "ID", 26: "ID", 28: "ID", 30: "ID", 32: "ID", 34:"ID", 36: "ID"}
#Gets the API Key and Secret
api_key = 'Secret ID'
api_secret = 'Secret Key'
mailjet = Client(auth=(api_key, api_secret), version='v3')

#gets all these company names along with the server number
with  open("SCSM_ExchangeServers.csv", "r") as f:
    companyreader = csv.DictReader(f)
    company_list = [ row["Subaccount HP Name"] for row in companyreader if ServerURL == row["Voice server"]]
    f.close()
#matches the server number with the server that is having an issue.
for j, k in company_dictionary.items():
    if int(j) == int(Server_number):
        id = k
#Once the script get te company server information, we will then input that information into the Mailjet service
for i in company_list:
    params = (('accountName', f'{i}'),)
    response = requests.get('https://Company.com/RestAPI/v1/api/accounts', headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    print(data)
    print(i)
    print("-"*10)
    for j in data["items"]:
        customerID = j["customerID"]

    email_response = requests.get(f'https://Company.com/RestAPI/v1/api/accounts/{customerID}/contacts', headers=headers)
    email_response.raise_for_status()
    emails = email_response.json()
    print(emails)
    
print("Done!")


