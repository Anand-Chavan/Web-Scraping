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
fp=open('American Academy Of Cosmetic Surgery-India.csv','w')
column=['firstname','lastname','degree','email','website','phoneNumber','address','pincode','place','country']
csvwriter = csv.writer(fp)
csvwriter.writerow(column)
docterNameArray=[]
url="https://www.cosmeticsurgery.org/search/custom.asp?id=2434"
p = re.compile(r'^(\s+)?(Mr(\.)?|Mrs(\.)?)?(?P<FIRST_NAME>.+)(\s+)(?P<LAST_NAME>.+)$', re.IGNORECASE)
driver = webdriver.Chrome(executable_path='chromedriver')
driver.get(url)
driver.find_element_by_xpath('//*[@id="txt_country"]').click()
driver.find_element_by_xpath('//*[@id="txt_country"]/option[105]').click()
driver.find_element_by_xpath('//*[@id="main"]/table/tbody/tr[6]/td[2]/input').click()
iframe=driver.find_element_by_xpath('//*[@id="SearchResultsFrame"]')
newUrl=iframe.get_attribute('src')
driver.get(newUrl)
urls=[]
links=driver.find_elements_by_tag_name('a')
for link in links:
	check=link.get_attribute('href')
	if(check!=None):
		if('member' in check):
			urls.append(check)

for check in urls:
	driver.get(check)
	dname=""
	email=""
	address=""
	phoneNumber=""
	website=""

	try:
		dname=driver.find_element_by_xpath('//*[@id="SpTitleBar"]').text 
	except:
		dname=""

	try:
		email=driver.find_element_by_xpath('//*[@id="SpContent_Container"]/table/tbody/tr[2]/td[3]/table[1]/tbody/tr/td/a').text
	except:
		email=""

	try:
		address=driver.find_element_by_xpath('//*[@id="tdEmployerName"]').text
	except:
		address=""

	try:
		phoneNumber=driver.find_element_by_xpath('//*[@id="tdWorkPhone"]').text
	except:
		phoneNumber=""

	try:
		website=driver.find_element_by_xpath('//*[@id="tdWorkPhone"]/a').get_attribute('href')
	except:
		website=""


	addressArray=address.split('\n')
	address=""
	for j in range(0,len(addressArray)):
		address=address+' '+addressArray[j]

	address=address[0:len(address)-8]
	docterNameArray=dname.split(' ')
	firstname=docterNameArray[0]
	lastname=docterNameArray[1]
	degree=""
	for m in range(2,len(docterNameArray)):
		degree=degree+docterNameArray[m]

	places = GeoText(address)
	city=places.cities
	place=""
	if(city!=[]):
		place=city[0]

	pincode=""
	reg = re.compile('^.*(?P<zipcode>\d{6}).*$')
	match = reg.match(address)

	if(match):
		pincode=match.groupdict()['zipcode']


	if(phoneNumber!=None):
		phoneNumber=re.sub('[^0-9]+', '',phoneNumber)
		if(len(phoneNumber)>=8):
			phoneNumber=phonenumbers.format_number(phonenumbers.parse(phoneNumber, 'IN'), phonenumbers.PhoneNumberFormat.NATIONAL)
			phoneNumber='+91'+phoneNumber[1:len(phoneNumber)]

	column=[firstname,lastname,degree,email,website,phoneNumber,address,pincode,place,'IN']
	csvwriter = csv.writer(fp)
	csvwriter.writerow(column)




