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
from selenium.common.exceptions import NoAlertPresentException
# from selenium.webdriver.support.ui import WebDriverWait
import pyap
import time
from geotext import GeoText
url='https://cao-aco.org/find-an-orthodontist/'
driver = webdriver.Chrome(executable_path='chromedriver')
driver.get(url)
driver.implicitly_wait(10)
driver.find_element_by_xpath('//*[@id="cn-accept-cookie"]').click()
driver.implicitly_wait(10)
driver.find_element_by_xpath('//*[@id="post-313"]/div/div/div/div/div[1]/div[2]/div[1]/ul/li[2]/a').click()
driver.find_element_by_xpath('//*[@id="provinceSelectBoxItArrow"]').click()
for k in range(2,16):
	selectProvision='//*[@id="provinceSelectBoxItOptions"]/li['+str(k)+']/a'
	driver.find_element_by_xpath(selectProvision).click()











# fp=open('Canadian Association of Orthodontists.csv','w')
# column=['fname','lname','Address1','Address2','city','state','zipcode','country','phoneNumber','Fax','Website','status','Date_Joined']
# csvwriter = csv.writer(fp)
# csvwriter.writerow(column)