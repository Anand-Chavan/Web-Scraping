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
docterNameArray=[]
fp=open("American Society for dermatologic-surgeon UAE.csv","w")
column=['firstname','Lastname','degrees','address','pincode','city',"country",'phoneNumber',"website"]
csvwriter = csv.writer(fp)
csvwriter.writerow(column)

url="https://www.asds.net/find-a-dermatologic-surgeon/advanced/true"
p = re.compile(r'^(\s+)?(Mr(\.)?|Mrs(\.)?)?(?P<FIRST_NAME>.+)(\s+)(?P<LAST_NAME>.+)$', re.IGNORECASE)
driver = webdriver.Chrome(executable_path='chromedriver')
driver.get(url)
driver.find_element_by_xpath('//*[@id="advanced-ountry7608-1242"]').click()
driver.find_element_by_xpath('//*[@id="advanced-ountry7608-1242"]/option[2]').click()
driver.find_element_by_xpath('//*[@id="dnn_ctr7608_Search_LocatorSearch"]/div/div[2]/div/div[6]/button[1]').click()
# //*[@id="advanced-ountry7608-1242"]/option[45]
for pagination in range(0,128):
	data=driver.find_elements_by_xpath('//*[@id="dnn_ctr7610_SearchResults_LocatorSearchResults"]')
	newData=data[0].find_elements_by_xpath('//*[@id="dnn_ctr7610_SearchResults_LocatorSearchResults"]/div/div[2]')
	for i in range(0,25):
		time.sleep(5)
		string='//*[@id="dnn_ctr7610_SearchResults_LocatorSearchResults"]/div/div[2]/div['+str(i+1)+']'
		content=newData[0].find_elements_by_xpath(string)
		time.sleep(2)
		# print(content)

		overallData=content[0].text.split('\n')
		# print(len(overallData))
		dname=overallData[1]
		print(dname)
		if(',' in dname):
			split1=dname.split(',')
			degree=split1[1]
			split2=split1[0].split(' ')
			firstname=split2[0]
			lastname=split2[len(split2)-1]
		else:
			split1=dname.split(' ')
			firstname=split1[0]
			lastname=split1[1]
			degree=""
		# //*[@id="dnn_ctr7610_SearchResults_LocatorSearchResults"]/div/div[2]/div[2]/div/div[1]
		string2='//*[@id="dnn_ctr7610_SearchResults_LocatorSearchResults"]/div/div[2]/div['+str(i+1)+']/div/div[1]'
		val=content[0].find_elements_by_xpath(string2)
		value=val[0].text
		address_array=value.split('\n')
		address=""
		for m in range(1,len(address_array)-2):
			if('Phone:' not in address_array[m]):
				address=address+address_array[m]
				address=address+" "
		if(address!=None):
			zipcode = re.search(r'\d{5}(?:-\d{4})?(?=\D*$)', address)
			if(zipcode!=None):
				pincode=zipcode.group()
			else:
				pincode="-"
			
		places = GeoText(address)
		city=places.cities
		place=""
		if(city!=[]):
			place=city[0]

		phoneNumber=""
		website=""
		Array=val[0].find_elements_by_tag_name('a')
		if(len(Array)>=2):
			phoneNumber=phonenumbers.format_number(phonenumbers.parse(Array[0].text, 'AE'), phonenumbers.PhoneNumberFormat.NATIONAL)
			phoneNumber=re.sub('[^0-9]+', '',Array[0].text)
			# phoneNumber=phoneNumber[1:len(phoneNumber)]
			phoneNumber='+'+phoneNumber
			website=Array[1].text

		csvwriter = csv.writer(fp)
		csvwriter.writerow([firstname,lastname,degree,address,pincode,place,'UAE',phoneNumber,website])
	# //*[@id="dnn_ctr7610_SearchResults_LocatorSearchResults"]/div/div[3]/div/ul/li[2]/button
	# //*[@id="dnn_ctr7610_SearchResults_LocatorSearchResults"]/div/div[3]/div/ul/li[3]/button
	# //*[@id="dnn_ctr7610_SearchResults_LocatorSearchResults"]/div/div[3]/div/ul/li[2]
	# //*[@id="dnn_ctr7610_SearchResults_LocatorSearchResults"]/div/div[3]/div/ul/li[2]
	# //*[@id="dnn_ctr7610_SearchResults_LocatorSearchResults"]/div/div[3]
	button='//*[@id="dnn_ctr7610_SearchResults_LocatorSearchResults"]/div/div[3]/div/ul/li['+str(pagination+2)+']'
	print(button)
	time.sleep(4)
	driver.find_element_by_xpath(button).click()
	time.sleep(4)

# //*[@id="dnn_ctr7610_SearchResults_LocatorSearchResults"]/div/div[3]/div/ul/li[2]/button
# //*[@id="dnn_ctr7610_SearchResults_LocatorSearchResults"]/div/div[3]/div/ul/li[3]/button
# string1='//*[@id="dnn_ctr7610_SearchResults_LocatorSearchResults"]/div/div[2]/div['+str(i+1)+']/div/div[1]/span[6]/a'
# 	string2='//*[@id="dnn_ctr7610_SearchResults_LocatorSearchResults"]/div/div[2]/div['+str(i+1)+']/div/div[1]/span[7]/a'
# 	phone=val[0].find_elements_by_xpath(string1)
# 	phoneNumber='+91'+phone[0].text
# 	mail=val[0].find_elements_by_xpath(string2)
# 	website=mail[0].text