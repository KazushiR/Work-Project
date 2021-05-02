import sys
sys.path.append(r"C:\Users\Name\Desktop\PythonProjects\Company_Name\Company State Locations")
from Server_Locations import Tokien_ID
import csv, os, requests
from mailjet_rest import Client
os.chdir(r"C:\Users\Name\Desktop\PythonProjects\Company_Name\Company Full Server List")
#makes a client ID and Secret for Mailjet
api_key = 'Client ID'
api_secret = 'Client Secret'
mailjet = Client(auth=(api_key, api_secret), version='v3')

#creates a dictionary of states to add to the mailjet email system
State_Dictionary = {"Arizona": ID, "California": ID, "Colorado": ID, "Idaho": ID, "Oregon": ID, "Washington": ID}

#opens up a CSV file for to get the accout ID for each company
with open("Company.csv") as f:
    Company_dict = csv.DictReader(f)
    Companies = [i["Account ID"] for i in Company_dict]
    f.close()

#makes a header for the company website
headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {Tokien_ID}'
    ,
}

while True:
    #if there is an HTTP Error due to not being able to pull the company information up properly, then it continues the script
    try:
        for i in Companies:
            print(i)
            #lets me know what company is being worked up and sends a request to the company website in a json format 
            params = (('customerID', f'{i}'),)
            response = requests.get('Company_Website', headers=headers, params=params)
            print(response)
            response.raise_for_status()
            #gets the state location of the company
            data = response.json()
            keys =next(iter(data.items()))[1]
            response_state = requests.get(f'https://Company_Website/{keys}/company', headers=headers)
            response_state.raise_for_status()
            print(response_state)
            #Gets the email of the company for the mailjet service
            request_email = requests.get(f'https://Company_Websites/{keys}/contacts', headers=headers)
            request_email.raise_for_status()
            print(request_email)
            emails = request_email.json()
            state = response_state.json()
            #If there is an address, then it gets the location of the state
            STATE = ','.join([value"state"] for key , value in state.items() if key == "address"])
            print(STATE)

            #this portion matchesemail up the state and puts the email into the correct contact list. From there, if there is a contact with our company email address, it will exclude that in the contact list and add it to the Mailjet Service
            for key, value in State_Dictionary.items():
                if key == STATE:
                    id = value
            for i in emails["items"]:
                if not i["email"].endswith("@MyCompany.com"):
                    print(i["email"])
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
        break
    except requests.exceptions.HTTPError:
        print(i)
        continue


print(result.status_code)
print(result.json())
print("Done!")
