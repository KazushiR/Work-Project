from selenium import webdriver
import os, re, smtplib
from selenium.webdriver.common.keys import Keys
from itertools import groupby
from datetime import datetime

os.environ["PATH"] = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"
browser = webdriver.Chrome(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\chromedriver.exe")
website = browser.get('https://Companywebsite.com')

#today's date
time = datetime.now().strftime('%m/%w/%Y')

#email definition
def email(time, finalimpacted):
    smtpobj = smtplib.SMTP("smtp.email.com", 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.login("MyEmail", "Password")
    smtpobj.sendmail("My Email", "MY Work Email",f"Subject: test 9 Company scheduled updates and maintence. {time}\n\n{finalimpacted}")
    smtpobj.close()
    
#Logging into website
browser.find_element_by_class_name("login-input").send_keys("MyName")
browser.find_element_by_class_name("password-input").send_keys("MyPassword")
browser.find_element_by_class_name("login-submit").click()
website2 = browser.get("https://My Company.com")

#getting and parsing information on companies
im = browser.find_elements_by_tag_name("tr")
impacted = [i.text for i in im]
finalimpacted = "\n\n".join(impacted)
emailimpacted = finalimpacted.encode('utf-8').decode('ascii', 'ignore')

#starttime
start = re.compile(r"Start Time:(.*)$")
startc = list(filter(start.search, impacted))

#endtime
end = re.compile(r"End Time:(.*)$")
endc = list(filter(end.search, impacted))


#Find Dates
dates = re.compile(r"CC(.*)$")
date2 = list(filter(dates.search,impacted))

#Downtimes
down = re.compile(r"Expected Downtime(.*)$")
downtime = list(filter(dates.search,impacted))

#list of dates and start times and end times
startlist = list(filter(lambda x : x, startc))
endlist = list(filter(lambda x : x, endc))
list1= list(filter(lambda x : x, date2))

#start+end
final = list(map(lambda x, y: x+ "\n" + y, startlist, endlist))
finalproduct = list(map(lambda x, y: ("-"*5)+ x+("-"*5) + "\n\n" +  y, list1, final))          
finallist = "\n\n".join(finalproduct)

#impacted companies
pattern = re.compile(r"Impacted Accounts: .*")
matches = pattern.findall(finalimpacted)
impactedcompanies = [i for i in matches]

browser.close()

new_companies = []

notwanted = "Impacted Accounts: "

Company_data = [i.replace("Impacted Accounts: ", '') for i in impactedcompanies]

os.chdir(r"C:\Users\MyName\Desktop\PythonProjects\Company Name\Selenium Work API")


file = open("Updates.txt", "w")
file.write(str(Company_data))
file.close()
