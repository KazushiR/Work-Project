import sys
#gets the tokien ID to access the API and get comapny ID's
sys.path.append(r"C:\Users\Name\Desktop\PythonProjects\Company API\Company State Locations")
from Server_Locations import Tokien_ID
import requests, os, csv
from collections import defaultdict
from mailjet_rest import Client

#matches the company ID's with whatever is in the company list in the Excel sheet.
os.chdir(r"C:\Users\Name\Desktop\PythonProjects\Company API\Company Full Server List")

#opens up the CSV file to read information on each company
with open("Company.csv", "r") as f:
    companyreader = csv.reader(f)
    next(companyreader)
    all_companies = [ row[1] for row in companyreader]
    f.close()

#sends a header to the API with the tokien ID
headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {Tokien_ID}',
}

#uses the secret keys to access Mailjet to send emails to customers
api_key = 'Client Secret'
api_secret = 'Client ID'
mailjet = Client(auth=(api_key, api_secret), version='v3')
id = 'ID'

for i in all_companies:
    #Gets the company name and from there, inpliment uses the CSV file to look up the company name
    params = 
        ('accountName', f'{i}'),
    )
    #company URL to find company ID and puts it in a json format
    response = requests.get('Work URL', headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    print(f"working on {i}")
    
    for i in data["items"]:
        customerID = i["customerID"]
    
    response2 = requests.get(f'Work URL', headers=headers)
    response2.raise_for_status() 
    data = response2.json()
    #gets the email of each invdividual within the company and adds it to the mailjet email list to send to customers later
    for i in data["items"]:
        if not i["email"].endswith("@MyWork.com"):
            emails = i["email"]
            print(f"Adding this email {emails} to Mailjet")
            data = {
              'Action': "addnoforce",
              'Contacts': [
                {
                  "Email": f"{emails}",
                  "IsExcludedFromCampaigns": "false",
                  "Name": "Passenger 1",
                  "Properties": "object"
                }
              ]
            }
            result = mailjet.contactslist_managemanycontacts.create(id=id, data=data)
print(result.status_code)
print(result.json())










