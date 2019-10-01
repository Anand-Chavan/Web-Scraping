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
import pyap
import time
from geotext import GeoText
fp=open('International-Society-Of-Orthodentics.csv','w')
column=['fname','lname','Address1','Address2','city','state','zipcode','country','phoneNumber','Fax','Website','status','Date_Joined']
csvwriter = csv.writer(fp)
csvwriter.writerow(column)
url='https://www.iaortho.org/new-page'
driver = webdriver.Chrome(executable_path='chromedriver')
driver.get(url)
tableData=driver.find_elements_by_class_name('table-row')
k=1
for content in tableData:
	fname=content.find_element_by_xpath('//*[@id="block-yui_3_17_2_1_1536605966412_4356"]/div/table/tbody/tr['+str(k)+']/td[2]').text
	lname=content.find_element_by_xpath('//*[@id="block-yui_3_17_2_1_1536605966412_4356"]/div/table/tbody/tr['+str(k)+']/td[3]').text
	Address1=content.find_element_by_xpath('//*[@id="block-yui_3_17_2_1_1536605966412_4356"]/div/table/tbody/tr['+str(k)+']/td[4]').text
	Address2=content.find_element_by_xpath('//*[@id="block-yui_3_17_2_1_1536605966412_4356"]/div/table/tbody/tr['+str(k)+']/td[5]').text
	city=content.find_element_by_xpath('//*[@id="block-yui_3_17_2_1_1536605966412_4356"]/div/table/tbody/tr['+str(k)+']/td[6]').text
	state=content.find_element_by_xpath('//*[@id="block-yui_3_17_2_1_1536605966412_4356"]/div/table/tbody/tr['+str(k)+']/td[7]').text
	zipcode=content.find_element_by_xpath('//*[@id="block-yui_3_17_2_1_1536605966412_4356"]/div/table/tbody/tr['+str(k)+']/td[8]').text
	country=content.find_element_by_xpath('//*[@id="block-yui_3_17_2_1_1536605966412_4356"]/div/table/tbody/tr['+str(k)+']/td[9]').text
	phoneNumber=content.find_element_by_xpath('//*[@id="block-yui_3_17_2_1_1536605966412_4356"]/div/table/tbody/tr['+str(k)+']/td[10]').text
	Fax=content.find_element_by_xpath('//*[@id="block-yui_3_17_2_1_1536605966412_4356"]/div/table/tbody/tr['+str(k)+']/td[11]').text
	Email=content.find_element_by_xpath('//*[@id="block-yui_3_17_2_1_1536605966412_4356"]/div/table/tbody/tr['+str(k)+']/td[12]').text
	Website=content.find_element_by_xpath('//*[@id="block-yui_3_17_2_1_1536605966412_4356"]/div/table/tbody/tr['+str(k)+']/td[13]').text
	status=content.find_element_by_xpath('//*[@id="block-yui_3_17_2_1_1536605966412_4356"]/div/table/tbody/tr['+str(k)+']/td[14]').text
	Date_Joined=content.find_element_by_xpath('//*[@id="block-yui_3_17_2_1_1536605966412_4356"]/div/table/tbody/tr['+str(k)+']/td[15]').text
	print(fname,lname)
	k=k+1
	column=[fname,lname,Address1,Address2,city,state,zipcode,country,phoneNumber,Fax,Website,status,Date_Joined]
	csvwriter = csv.writer(fp)
	csvwriter.writerow(column)

# driver.find_element_by_xpath('//*[@id="aaRflssareferralCountry"]/select').click()
# driver.find_element_by_xpath('//*[@id="aaRflssareferralCountry"]/select/option[110]').click()
