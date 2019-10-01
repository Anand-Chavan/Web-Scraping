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
p = re.compile(r'^(\s+)?(Mr(\.)?|Mrs(\.)?)?(?P<FIRST_NAME>.+)(\s+)(?P<LAST_NAME>.+)$', re.IGNORECASE)

docterNameArray=[]
fp=open('perio-UAE.csv',"w")
column=['first_name','last_name','address','pincode','city','Country','email','phoneNumber','web']
csvwriter = csv.writer(fp)
csvwriter.writerow(column)
url="https://www.perio.org/?q=locator-advanced"
driver = webdriver.Chrome(executable_path='chromedriver')
driver.get(url)
driver.find_element_by_xpath('//*[@id="block-system-main"]/div/div/div[1]/div/div/form[3]/select').click()
driver.find_element_by_xpath('//*[@id="block-system-main"]/div/div/div[1]/div/div/form[3]/select/option[77]').click()
driver.find_element_by_xpath('//*[@id="block-system-main"]/div/div/div[1]/div/div/form[3]/input[2]').click()
ptag=2
links=driver.find_elements_by_tag_name('a')
for link in links:
	if(link.get_attribute('target')=="_blank"):
		intialData=driver.find_element_by_xpath('//*[@id="block-system-main"]/div/div/div[1]/div/div/p['+str(ptag)+']').text
		splitInitialData=intialData.split('\n')
		dname=splitInitialData[0]
		address=splitInitialData[1]
		phoneNumber=""
		if(len(splitInitialData)>2):
			phoneNumber=splitInitialData[2]
		try:
			url=link.get_attribute('href')
			result=requests.get(url)
			src = result.content
			soup = BeautifulSoup(src, "lxml")
			link=soup.find('div',{'class':'row'})
			web=""
			email=""
			email=link.find('a')
			if(email!=None):
				email=email.text
			web=link.find('a',{"target":"_blank"})
			if(web!=None):
				web=web.text
			
		except:
			NoAction=0
			
		finally:
			# driver2.close()
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
			if(len(phoneNumber)>=8):
				phoneNumber=phonenumbers.format_number(phonenumbers.parse(phoneNumber, 'AE'), phonenumbers.PhoneNumberFormat.NATIONAL)
				phoneNumber='+971'+phoneNumber[1:len(phoneNumber)]

			if(')' in phoneNumber):
				phoneNumber=re.sub('[^0-9]+', '',phoneNumber)
				phoneNumber='+'+phoneNumber
			print(phoneNumber,email,web)
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


			if(dname not in docterNameArray):
				docterNameArray.append(dname)
				column=[first_name,last_name,address,pincode,place,'UAE',email,phoneNumber,web]
				csvwriter = csv.writer(fp)
				csvwriter.writerow(column)

			print(dname)
						# driver2.close()
		ptag=ptag+1
