import sys
import requests
import csv
from bs4 import BeautifulSoup
import phonenumbers
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pyap
import time
from geotext import GeoText
url='https://en.wikipedia.org/wiki/List_of_cities_in_the_United_Kingdom'
# //*[@id="mw-content-text"]/div/table[2]/tbody/tr[66]/td[1]
# url='http://www.dubaifaqs.com/list-of-cities-uae.php'
driver = webdriver.Chrome(executable_path='chromedriver')
driver.get(url)
# data=driver.find_elements_by_xpath('/html/body/div/table/tbody/tr[3]/th')

# # /html/body/div/table/tbody/tr[4]/th
# # /html/body/div/table/tbody/tr[34]/td[1]
# k=16
# # for k in range(16,35):
# # 	string='/html/body/div/table/tbody/tr['+str(k)+']/td[1]'
# # 	cityName=driver.find_element_by_xpath(string).text 
# # 	print(cityName)
# for k in range(4,23):
# 	string='/html/body/div/table/tbody/tr['+str(k)+']/td[1]'
# 	cityName=driver.find_element_by_xpath(string).text 
# 	print(cityName)
# # /html/body/div/table/tbody/tr[17]/td[1]

for i in range(1,67):
	string='//*[@id="mw-content-text"]/div/table[2]/tbody/tr['+str(i)+']/td[1]'
	name=driver.find_element_by_xpath(string).text
	name=re.sub('[^a-zA-Z]+', '',name)
	print(name)
	