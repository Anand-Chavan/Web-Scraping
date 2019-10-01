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
fp=open('AAE-UK.csv','w')
column=['FirstName','LastName','Degree','Address','Pincode','City','Country','PhoneNumber','Website']
csvwriter = csv.writer(fp)
csvwriter.writerow(column)
p = re.compile(r'^(\s+)?(Mr(\.)?|Mrs(\.)?)?(?P<FIRST_NAME>.+)(\s+)(?P<LAST_NAME>.+)$', re.IGNORECASE)
docterNameArray=[]
url='https://ams.aae.org/aaessa/rflssareferral.query_page?p_session_serno=1147451&p_cust_id=&p_vendor_ty=ENDO&p_advanced=Y&p_context='
driver = webdriver.Chrome(executable_path='chromedriver')
driver.get(url)
driver.find_element_by_xpath('//*[@id="aaRflssareferralCountry"]/select').click()
driver.find_element_by_xpath('//*[@id="aaRflssareferralCountry"]/select/option[240]').click()
driver.find_element_by_xpath('//*[@id="aaRflssareferralDistance"]/select').click()
driver.find_element_by_xpath('//*[@id="aaRflssareferralDistance"]/select/option[1]').click()
driver.find_element_by_xpath('//*[@id="aaRflssareferralRowsPP"]/select').click()
driver.find_element_by_xpath('//*[@id="aaRflssareferralRowsPP"]/select/option[1]').click()
driver.find_element_by_xpath('//*[@id="aaRflssareferralSubmit"]').click()
# alert = world.browser.switch_to.alert
driver.switch_to_alert().accept()
k=1
data=driver.find_elements_by_class_name('aaRflResultWrapper')
for content in data:
	dname_xpath='//*[@id="aaRflSearchVendorSummary"]/div['+str(k)+']/ul/li[1]/a'
	initial=content.find_element_by_xpath(dname_xpath).text 
	phoneNumberArray=content.find_element_by_id('aaRflVendorDetailPhoneFaxEmailWeb').text
	address_xpath='//*[@id="aaRflSearchVendorSummary"]/div['+str(k)+']/ul/li[2]'
	address=content.find_element_by_xpath(address_xpath).text
	splitData=initial.split(',')
	dname=splitData[0]
	degree=""
	for ml in range(2,len(splitData)):
		degree=degree+splitData[ml]

	if('(Dr.)' in dname):
		dname=dname.replace("Dr.","")

	if('Dr.' in dname):
		dname=dname.replace("Dr.","")

	if('Prof.' in dname):
		dname=dname.replace("Dr.","")


	m = p.match(dname)
	first_name=""
	last_name=""
	if(m != None):
		first_name = m.group('FIRST_NAME')
		last_name = m.group('LAST_NAME')

	extract=phoneNumberArray.split('\n')
	website=""
	phoneNumber=extract[0]
	if(len(extract)>=2):
		website=extract[1]
		website=website[5:len(website)]
	phoneNumber=re.sub('[^0-9]+', '',phoneNumber)
	if(len(phoneNumber)>=8):
		phoneNumber=phonenumbers.format_number(phonenumbers.parse(phoneNumber, 'GB'), phonenumbers.PhoneNumberFormat.NATIONAL)
		phoneNumber='+44'+phoneNumber[1:len(phoneNumber)]

	if(')' in phoneNumber):
		phoneNumber=re.sub('[^0-9]+', '',phoneNumber)
		phoneNumber='+'+phoneNumber

	places = GeoText(address)
	city=places.cities
	place=""
	if(city!=[]):
		place=city[0]

	# pincode=""
	# reg = re.compile('^.*(?P<zipcode>\d{6}).*$')
	# match = reg.match(address)

	# if(match):
	# 	pincode=match.groupdict()['zipcode']
	pincode=""
	if(address!=None):
		zipcode = re.search(r'\d{6}(?:-\d{4})?(?=\D*$)', address)
		if(zipcode!=None):
			pincode=zipcode.group()
		else:
			pincode="-"
	print(pincode)


	if(dname not in docterNameArray):
		docterNameArray.append(dname)
		column=[first_name,last_name,degree,address,pincode,place,'GB',phoneNumber,website]
		csvwriter = csv.writer(fp)
		csvwriter.writerow(column)
	k=k+1