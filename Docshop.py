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
import time
from geotext import GeoText
url="https://www.docshop.com/"
driver = webdriver.Chrome(executable_path='chromedriver')
driver.get(url)
driver.find_element_by_xpath('//*[@id="search_specialty"]').click()
for k in range(2,10):
	xpath='//*[@id="search_specialty"]/option['+str(k+1)+']'
	driver.find_element_by_xpath('//*[@id="search_specialty"]').click()
	time.sleep(1)
	speciality=driver.find_element_by_xpath(xpath).text
	if(speciality=="Bariatric Surgery"):
		dname=""
	