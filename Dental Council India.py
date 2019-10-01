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
fp=open('Dental-Council-India.csv','w')
column=['firstname','lastname','email','phoneNumber','address','pincode','place','state','Country']
csvwriter = csv.writer(fp)
csvwriter.writerow(column)
url="http://dciindia.gov.in/CouncilMember.aspx"
driver = webdriver.Chrome(executable_path='chromedriver')
driver.get(url)
table1=driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[1]')
tabledata1=table1.find_elements_by_tag_name('tr')
row=5
while(row<=len(tabledata1)):
	string='//*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[1]/tbody/tr['+str(row+1)+']/td[2]'
	raw_address=tabledata1[row].find_element_by_xpath(string).text
	split_text=raw_address.split('\n')
	docterName=""

	if('(Dr.)' in split_text[0]):
		docterName=split_text[0].replace("Dr.","")

	if('Dr.' in split_text[0]):
		docterName=split_text[0].replace("Dr.","")

	if('Prof.' in split_text[0]):
		docterName=split_text[0].replace("Dr.","")


	docterNameArray=docterName.split(' ')
	firstname=docterNameArray[1]
	lastname=docterNameArray[len(docterNameArray)-1]
	address=""
	for k in range(2,len(split_text)):
		address=address+" "+split_text[k]

	xpath_for_city='//*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[1]/tbody/tr['+str(row+1)+']/td[4]'
	state=tabledata1[row].find_element_by_xpath(xpath_for_city).text
	xpath_for_contactInfo='//*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[1]/tbody/tr['+str(row+1)+']/td[8]'
	contactInfo=tabledata1[row].find_element_by_xpath(xpath_for_contactInfo).text
	contactInfoArray=contactInfo.split('\n')
	phoneArray=[]
	for k in range(0,len(contactInfoArray)):
		if('@' in contactInfoArray[k]):
			email=contactInfoArray[k]
		else:
			phoneArray.append(contactInfoArray[k])

	if('Email.:' in email):
		email=email.replace("Email.:","")

	if('Email:' in email):
		email=email.replace("Email:","")


	phoneNumber=re.sub('[^0-9]+', '',phoneArray[0])
	if(len(phoneNumber)>=8):
		phoneNumber=phonenumbers.format_number(phonenumbers.parse(phoneNumber, 'IN'), phonenumbers.PhoneNumberFormat.NATIONAL)
		phoneNumber='+91'+phoneNumber[1:len(phoneNumber)]

	places = GeoText(address)
	city=places.cities
	place=""
	if(city!=[]):
		place=city[0]

	pincode=""
	reg = re.compile('^.*(?P<zipcode>\d{5}).*$')
	match = reg.match(address)

	if(match):
		pincode=match.groupdict()['zipcode']

	column=[firstname,lastname,email,phoneNumber,address,pincode,place,state,'IN']
	csvwriter = csv.writer(fp)
	csvwriter.writerow(column)

	row=row+2


# //*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[3]
table2=driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[3]')
tabledata2=table2.find_elements_by_tag_name('tr')
row=5
while(row<=len(tabledata2)):
	print("-")
	try:
		string='//*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[3]/tbody[1]/tr['+str(row+1)+']/td[2]'
		raw_address=tabledata2[row].find_element_by_xpath(string).text
		split_text=raw_address.split('\n')
		docterName=""

		if('(Dr.)' in split_text[0]):
			docterName=split_text[0].replace("Dr.","")

		if('Dr.' in split_text[0]):
			docterName=split_text[0].replace("Dr.","")

		if('Prof.' in split_text[0]):
			docterName=split_text[0].replace("Dr.","")


		docterNameArray=docterName.split(' ')
		firstname=docterNameArray[1]
		lastname=docterNameArray[len(docterNameArray)-1]
		address=""
		for k in range(2,len(split_text)):
			address=address+" "+split_text[k]

		# //*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[3]/tbody[1]/tr[6]/td[4]
		xpath_for_city='//*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[3]/tbody[1]/tr['+str(row+1)+']/td[4]'
		state=tabledata2[row].find_element_by_xpath(xpath_for_city).text
		# //*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[3]/tbody[1]/tr[6]/td[4]
		xpath_for_contactInfo='//*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[3]/tbody[1]/tr['+str(row+1)+']/td[8]'
		contactInfo=tabledata2[row].find_element_by_xpath(xpath_for_contactInfo).text
		contactInfoArray=contactInfo.split('\n')
		phoneArray=[]
		for k in range(0,len(contactInfoArray)):
			if('@' in contactInfoArray[k]):
				email=contactInfoArray[k]
			else:
				phoneArray.append(contactInfoArray[k])

		if('Email.:' in email):
			email=email.replace("Email.:","")

		if('Email:' in email):
			email=email.replace("Email:","")


		if(',' not in phoneArray[0]):
			phoneNumber=re.sub('[^0-9]+', '',phoneArray[0])
		if(',' in phoneArray[0]):
			newText=phoneArray[0].split(',')
			phoneNumber=re.sub('[^0-9]+', '',newText[0])
			
		if(len(phoneNumber)>=8 and len(phoneNumber)<=12):
			phoneNumber=phonenumbers.format_number(phonenumbers.parse(phoneNumber, 'IN'), phonenumbers.PhoneNumberFormat.NATIONAL)
			phoneNumber='+91'+phoneNumber[1:len(phoneNumber)]

		places = GeoText(address)
		city=places.cities
		place=""
		if(city!=[]):
			place=city[0]

		pincode=""
		reg = re.compile('^.*(?P<zipcode>\d{5}).*$')
		match = reg.match(address)

		if(match):
			pincode=match.groupdict()['zipcode']

		column=[firstname,lastname,email,phoneNumber,address,pincode,place,state,'IN']
		csvwriter = csv.writer(fp)
		csvwriter.writerow(column)

		row=row+1
		print('try',row)
	except:
		row=row+1
		print('cache',row)


# //*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[4]
table2=driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[4]')
tabledata2=table2.find_elements_by_tag_name('tr')
row=6
while(row<=len(tabledata2)):
	print("-")
	try:
		# //*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[4]/tbody[1]/tr[7]/td[2]
		string='//*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[4]/tbody[1]/tr['+str(row+1)+']/td[2]'
		raw_address=tabledata2[row].find_element_by_xpath(string).text
		split_text=raw_address.split('\n')
		docterName=""

		if('(Dr.)' in split_text[0]):
			docterName=split_text[0].replace("Dr.","")

		if('Dr.' in split_text[0]):
			docterName=split_text[0].replace("Dr.","")

		if('Prof.' in split_text[0]):
			docterName=split_text[0].replace("Dr.","")

		docterNameArray=docterName.split(' ')
		firstname=docterNameArray[1]
		lastname=docterNameArray[len(docterNameArray)-1]
		address=""
		for k in range(2,len(split_text)):
			address=address+" "+split_text[k]

		# //*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[3]/tbody[1]/tr[6]/td[4]
		xpath_for_city='//*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[4]/tbody[1]/tr['+str(row+1)+']/td[4]'
		state=tabledata2[row].find_element_by_xpath(xpath_for_city).text
		# //*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[3]/tbody[1]/tr[6]/td[4]
		xpath_for_contactInfo='//*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[4]/tbody[1]/tr['+str(row+1)+']/td[8]'
		contactInfo=tabledata2[row].find_element_by_xpath(xpath_for_contactInfo).text
		contactInfoArray=contactInfo.split('\n')
		phoneArray=[]
		for k in range(0,len(contactInfoArray)):
			if('@' in contactInfoArray[k]):
				email=contactInfoArray[k]
			else:
				phoneArray.append(contactInfoArray[k])

		if('Email.:' in email):
			email=email.replace("Email.:","")

		if('Email:' in email):
			email=email.replace("Email:","")


		if(',' not in phoneArray[0]):
			phoneNumber=re.sub('[^0-9]+', '',phoneArray[0])
		if(',' in phoneArray[0]):
			newText=phoneArray[0].split(',')
			phoneNumber=re.sub('[^0-9]+', '',newText[0])

		if(len(phoneNumber)>=8 and len(phoneNumber)<=12):
			phoneNumber=phonenumbers.format_number(phonenumbers.parse(phoneNumber, 'IN'), phonenumbers.PhoneNumberFormat.NATIONAL)
			phoneNumber='+91'+phoneNumber[1:len(phoneNumber)]

		places = GeoText(address)
		city=places.cities
		place=""
		if(city!=[]):
			place=city[0]

		pincode=""
		reg = re.compile('^.*(?P<zipcode>\d{5}).*$')
		match = reg.match(address)

		if(match):
			pincode=match.groupdict()['zipcode']

		column=[firstname,lastname,email,phoneNumber,address,pincode,place,state,'IN']
		csvwriter = csv.writer(fp)
		csvwriter.writerow(column)

		row=row+1
		print('try',row)
	except:
		row=row+1
		print('cache',row)


table2=driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[5]')
tabledata2=table2.find_elements_by_tag_name('tr')
row=6
while(row<=len(tabledata2)):
	print("-")
	try:
		# //*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[4]/tbody[1]/tr[7]/td[2]
		string='//*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[5]/tbody[1]/tr['+str(row+1)+']/td[2]'
		raw_address=tabledata2[row].find_element_by_xpath(string).text
		split_text=raw_address.split('\n')
		docterName=""
		if('Dr.' in split_text[0]):
			docterName=split_text[0].replace("Dr.","")
		docterNameArray=docterName.split(' ')
		firstname=docterNameArray[1]
		lastname=docterNameArray[len(docterNameArray)-1]
		address=""
		for k in range(2,len(split_text)):
			address=address+" "+split_text[k]

		# //*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[3]/tbody[1]/tr[6]/td[4]
		xpath_for_city='//*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[4]/tbody[1]/tr['+str(row+1)+']/td[4]'
		state=tabledata2[row].find_element_by_xpath(xpath_for_city).text
		# //*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[3]/tbody[1]/tr[6]/td[4]
		xpath_for_contactInfo='//*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[5]/tbody[1]/tr['+str(row+1)+']/td[8]'
		contactInfo=tabledata2[row].find_element_by_xpath(xpath_for_contactInfo).text
		contactInfoArray=contactInfo.split('\n')
		phoneArray=[]
		for k in range(0,len(contactInfoArray)):
			if('@' in contactInfoArray[k]):
				email=contactInfoArray[k]
			else:
				phoneArray.append(contactInfoArray[k])

		if('Email.:' in email):
			email=email.replace("Email.:","")

		if('Email:' in email):
			email=email.replace("Email:","")

		if(',' not in phoneArray[0]):
			phoneNumber=re.sub('[^0-9]+', '',phoneArray[0])
		if(',' in phoneArray[0]):
			newText=phoneArray[0].split(',')
			phoneNumber=re.sub('[^0-9]+', '',newText[0])

		if(len(phoneNumber)>=8 and len(phoneNumber)<=12):
			phoneNumber=phonenumbers.format_number(phonenumbers.parse(phoneNumber, 'IN'), phonenumbers.PhoneNumberFormat.NATIONAL)
			phoneNumber='+91'+phoneNumber[1:len(phoneNumber)]

		places = GeoText(address)
		city=places.cities
		place=""
		if(city!=[]):
			place=city[0]

		pincode=""
		reg = re.compile('^.*(?P<zipcode>\d{5}).*$')
		match = reg.match(address)

		if(match):
			pincode=match.groupdict()['zipcode']

		column=[firstname,lastname,email,phoneNumber,address,pincode,place,state,'IN']
		csvwriter = csv.writer(fp)
		csvwriter.writerow(column)

		row=row+1
		print('try',row)
	except:
		row=row+1
		print('cache',row)


table2=driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[6]')
tabledata2=table2.find_elements_by_tag_name('tr')
row=6
while(row<=len(tabledata2)):
	print("-")
	try:
		# //*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[4]/tbody[1]/tr[7]/td[2]
		string='//*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[6]/tbody/tr['+str(row+1)+']/td[2]'
		raw_address=tabledata2[row].find_element_by_xpath(string).text
		split_text=raw_address.split('\n')
		docterName=""

		if('(Dr.)' in split_text[0]):
			docterName=split_text[0].replace("Dr.","")

		if('Dr.' in split_text[0]):
			docterName=split_text[0].replace("Dr.","")

		if('Prof.' in split_text[0]):
			docterName=split_text[0].replace("Dr.","")

		docterNameArray=docterName.split(' ')
		firstname=docterNameArray[1]
		lastname=docterNameArray[len(docterNameArray)-1]
		address=""
		for k in range(2,len(split_text)):
			address=address+" "+split_text[k]

		state=""
		# //*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[3]/tbody[1]/tr[6]/td[4]
		# xpath_for_city='//*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[4]/tbody[1]/tr['+str(row+1)+']/td[4]'
		# state=tabledata2[row].find_element_by_xpath(xpath_for_city).text
		# //*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[3]/tbody[1]/tr[6]/td[4]
		xpath_for_contactInfo='//*[@id="ctl00_ContentPlaceHolder3_pnlContents"]/div/div/div[2]/table[6]/tbody/tr['+str(row+1)+']/td[8]'
		contactInfo=tabledata2[row].find_element_by_xpath(xpath_for_contactInfo).text
		contactInfoArray=contactInfo.split('\n')
		phoneArray=[]
		for k in range(0,len(contactInfoArray)):
			if('@' in contactInfoArray[k]):
				email=contactInfoArray[k]
			else:
				phoneArray.append(contactInfoArray[k])

		if('Email.:' in email):
			email=email.replace("Email.:","")

		if('Email:' in email):
			email=email.replace("Email:","")

		if(',' not in phoneArray[0]):
			phoneNumber=re.sub('[^0-9]+', '',phoneArray[0])
		if(',' in phoneArray[0]):
			newText=phoneArray[0].split(',')
			phoneNumber=re.sub('[^0-9]+', '',newText[0])

		if(len(phoneNumber)>=8 and len(phoneNumber)<=12):
			phoneNumber=phonenumbers.format_number(phonenumbers.parse(phoneNumber, 'IN'), phonenumbers.PhoneNumberFormat.NATIONAL)
			phoneNumber='+91'+phoneNumber[1:len(phoneNumber)]

		places = GeoText(address)
		city=places.cities
		place=""
		if(city!=[]):
			place=city[0]

		pincode=""
		reg = re.compile('^.*(?P<zipcode>\d{5}).*$')
		match = reg.match(address)

		if(match):
			pincode=match.groupdict()['zipcode']

		column=[firstname,lastname,email,phoneNumber,address,pincode,place,state,'IN']
		csvwriter = csv.writer(fp)
		csvwriter.writerow(column)

		row=row+1
		print('try',row)
	except:
		row=row+1
		print('cache',row)

