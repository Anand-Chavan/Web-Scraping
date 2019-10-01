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

docterNameArray=[]
p = re.compile(r'^(\s+)?(Mr(\.)?|Mrs(\.)?)?(?P<FIRST_NAME>.+)(\s+)(?P<LAST_NAME>.+)$', re.IGNORECASE)

fp2=open("American Association Of OrthoDentist-UK.csv","w")
docterNameArray=[]
column=['firstname','Lastname','address','pincode','city',"country",'phoneNumber','website']
csvwriter = csv.writer(fp2)
csvwriter.writerow(column)

fp=open('UK-City.txt','r')
cities=fp.readlines()
for city in cities:
	print(city)		
	url='https://www.aaoinfo.org/locator?location='+str(city)+'&groupCode=&types='
	result=requests.get(url)
	src = result.content
	soup = BeautifulSoup(src, "lxml")
	docterList=soup.find_all('div',{"class":"record"})
	for data in docterList:
		dname=data.find('div',{'class':'name'}).text
		address=data.find('div',{'class':'doctor-info'}).text
		phoneNumber=data.find('div',{'class':'phone hidden-sm-down'})
		if(phoneNumber!=None):
			phoneNumber=phoneNumber.text

		website=data.find('div',{'class':'website'})
		if(website!=None):
			website=website.text
		
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

		phoneNumber=re.sub('[^0-9]+', '',phoneNumber)
		if(len(phoneNumber)>=8 and len(phoneNumber)<=12):
			phoneNumber=phonenumbers.format_number(phonenumbers.parse(phoneNumber, 'GB'), phonenumbers.PhoneNumberFormat.NATIONAL)
			phoneNumber='+44'+phoneNumber[1:len(phoneNumber)]

		# places = GeoText(address)
		# city=places.cities
		# place=""
		# if(city!=[]):
		# 	place=city[0]

		pincode=""
		reg = re.compile('^.*(?P<zipcode>\d{5}).*$')
		match = reg.match(address)

		if(match):
			pincode=match.groupdict()['zipcode']

		if(dname not in docterNameArray):
			docterNameArray.append(dname)
			column=[first_name,last_name,address,pincode,city,'UK',phoneNumber,website]
			csvwriter = csv.writer(fp2)
			csvwriter.writerow(column)


print(len(docterNameArray))







