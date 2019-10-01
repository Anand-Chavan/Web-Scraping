# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
import sys
import requests
import csv
from bs4 import BeautifulSoup
import phonenumbers
import re
# driver = webdriver.Chrome(executable_path='chromedriver')
# url = "https://ishrs.org/find-a-doctor/"
# driver.get(url)
# data=driver.find_element_by_xpath("""//*[@id="wpgmza_table_1"]/tbody""")
# print(data)

# # posts=driver.find_element_by_class_name("view-profile")
# # driver.findElement(By.name("Name Locator")).getAttribute("value")
# # print(posts)

# # for content in posts:
# # 	print(content)
# //*[@id="name-search"]/div[5]/div[1]/div/div/a[1]/h3
# //*[@id="name-search"]/div[5]/div[2]/div/div/a[1]/h3

result=requests.get("https://ishrs.org/find-a-doctor/")
src = result.content
soup = BeautifulSoup(src, "lxml")
phoneNumber=soup.find_all('p')
print(phoneNumber)