import sys
sys.path.append(r"C:\Users\Name\Desktop\PythonProjects\Company API\Company State Locations")
from Server_Locations import Tokien_ID
import os, requests, csv
from mailjet_rest import Client
#Gets the API request tokien
os.chdir(r"C:\Users\Name\Desktop\PythonProjects\Company API\Company Website update")
#Creates an empty dictionary to store to use later 
new_empty_companies = []
empty_emails = []

headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {Tokien_ID}',
}
#gets the company key and secret for the Mailjet Service
api_key = 'Company_Key'
api_secret = 'Company_secret'
mailjet = Client(auth=(api_key, api_secret), version='v3')
id = 'ID_Number'

#Gets updated information from our partners website and stores it as a text file
with open('Updates.txt', 'r') as files:
    company_list = files.read()
    files.close()
#splits up the information to read and parse through the text to get information on each company and adds it to the table
Company_split = company_list.split(",")
for i in Company_split:
    comma = i.replace("['", ' ')
    comma2 = comma.replace("']", '')
    space = comma2.replace(" " ,'')
    last_commas = space.replace("'", "")
    new_empty_companies.append(last_commas)

#Parses through the list of companies and from there, it sends a header request to get the emails of each customer and stores it in our Email service.
for i in new_empty_companies:
    #If an HTTP Error pops up due to not finding a company, it continues with the script
    try:
        
        print("-"*10)
        print(i)
        params = (
            ('accountName', f'{i}'),
        )
        response = requests.get('https://Companywebsite/RestAPI/v1/api/accounts', headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        for i in data["items"]:
            customerID = i["customerID"]
        response2 =  requests.get(f'https://Companywebsite/RestAPI/v1/api/accounts/{customerID}/contacts', headers=headers)
        response2.raise_for_status()
        data_email = response2.json()
        for i in data_email["items"]:
            if not i["email"].endswith("@mycompany.com"):
                empty_emails.append(i["email"])
                data = {
                  'Action': "addnoforce",
                  'Contacts': [
                    {
                      "Email": f"{i['email']}",
                      "IsExcludedFromCampaigns": "false",
                      "Name": "Monthly Updates",
                      "Properties": "object"
                    }
                  ]
                }
                result = mailjet.contactslist_managemanycontacts.create(id=id, data=data)

    except requests.exceptions.HTTPError:
        continue
#Lets me know if this portion of the script is done
print(result.status_code)
print(result.json())

#sometimes, there are blank emails so this goes through and removes any blank email from our email service
while True:
    done = input("Are you done with this? Would you like the emails removed? ")
    if done.lower()== "yes" or done.lower()== "y":
        for i in empty_emails:
            print(i)
            data = {
            'Action': "remove",
            'Contacts': [{
            "Email": f"{i}",
            "IsExcludedFromCampaigns": "false",
            "Name": "Passenger 1",
            "Properties": "object"
            }]}
            result = mailjet.contactslist_managemanycontacts.create(id=id, data=data)
        break
    else:
        continue
print(result.status_code)
print(result.json())


