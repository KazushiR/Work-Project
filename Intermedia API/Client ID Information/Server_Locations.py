from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
browser.get('https://Company Website')

#goes to the company website and remotes in and gets company ID's from the website and saves it
browser.find_element_by_id("input_clientID").send_keys("TOKEN_ID")
browser.find_element_by_id("input_clientSecret").send_keys("TOKEN_SECRET")
time.sleep(1)
browser.find_element_by_id("button_requestToken").click()
time.sleep(1)
browser.find_element_by_id("explore").click()
Tokien_ID = browser.find_element_by_id("input_apiKey").get_attribute("value")
print(Tokien_ID)
browser.close()

