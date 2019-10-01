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

fp=open("Ishrs-USA.csv","w")
docterNameArray=[]
column=['firstname','Lastname','degrees','address','pincode','city',"country",'phoneNumber','email',"link"]
csvwriter = csv.writer(fp)
csvwriter.writerow(column)

docterNameArray=[]
url="https://ishrs.org/find-a-doctor/"
p = re.compile(r'^(\s+)?(Mr(\.)?|Mrs(\.)?)?(?P<FIRST_NAME>.+)(\s+)(?P<LAST_NAME>.+)$', re.IGNORECASE)

driver = webdriver.Chrome(executable_path='chromedriver')
# data=soup.find_all("div",{"class":"wpb_wrapper"})
# print(len(data))
# for content in data:
# 	newdata=content.find_all("div",{"class":"wpb_text_column wpb_content_element "})
# 	print(newdata)//*[@id="wpgmza_table_1"]/tbody
driver.get(url)
driver.find_element_by_id("name-search-button").click()
# time.sleep(2)
driver.find_element_by_xpath("""//*[@id="advanced-search-country"]""").click()
# time.sleep(2)
driver.find_element_by_xpath("""//*[@id="advanced-search-country"]/option[233]""").click()
# time.sleep(2)
# names=driver.find_element_by_tag_name('h3').find_elements_by_class_name('ng-binding')
# print(names)
# time.sleep(2)
# driver.
# get_div = driver.find_element_by_css_selector('p')
# print(get_div.text)
# //*[@id="name-search"]/div[5]/div[1]/div/div/p[3]
# //*[@id="name-search"]/div[3]/button[4]
# //*[@id="name-search"]/div[3]/button[5]
# //*[@id="name-search"]/div[3]/button[4]
start=4
newlink=driver.find_element_by_xpath('//*[@id="name-search"]/div[3]/span')
# newlink=driver.find_element_by_xpath('//*[@id="name-search"]/div[6]/button[6]')
for k in range(0,11):
	phoneNumber=""
	email=""
	# if(k<=6):
	newlink.click()
	# else:
	# 	click='//*[@id="name-search"]/div[3]/button['+str(start)+']'
	# 	newlink=driver.find_element_by_xpath('//*[@id="name-search"]/div[3]/button[4]').click()
	# 	start=start+1
		
	print(k)
	# print(newlink)
	links =driver.find_elements_by_class_name('view-profile')
	address=""
	for i in range(0,len(links)):
		link=links[i].get_attribute("href")
		result=requests.get(link)
		src = result.content
		soup = BeautifulSoup(src, "lxml")
		if(soup!=None):
			phoneNumber=soup.find('a',{'class':'call-user'})
			if(phoneNumber!=None):
				phoneNumber=phoneNumber.attrs['href']
			email=soup.find('a',{'class':'email-user'})
			if(email!=None):
				email=email.attrs['data-email']
				
		dname_xpath='//*[@id="name-search"]/div[5]/div['+str(i+1)+']/div/div/a[1]/h3'
		dname=driver.find_element_by_xpath(dname_xpath).text
		Array=dname.split(',')

		m = p.match(Array[0])
		first_name=""
		last_name=""
		if(m != None):
			first_name = m.group('FIRST_NAME')
			last_name = m.group('LAST_NAME')
		if('Dr.' in first_name):
			first_name=first_name.replace("Dr.","")
		elif('Dr .' in first_name):
			first_name=first_name.replace("Dr","")
		elif('Dr' in first_name):
			first_name=first_name.replace("Dr","")

		degree=""
		for j in range(1,len(Array)):
			degree=degree+Array[j]
		# print(first_name,last_name)
		if(phoneNumber!=None):
			phoneNumber=phonenumbers.format_number(phonenumbers.parse(phoneNumber, 'IN'), phonenumbers.PhoneNumberFormat.NATIONAL)
			phoneNumber='+1'+phoneNumber[1:len(phoneNumber)]
		add_xpath='//*[@id="name-search"]/div[5]/div['+str(i+1)+']/div/div/p[3]'
		address=driver.find_element_by_xpath(add_xpath).text
		add_xpath='//*[@id="name-search"]/div[5]/div['+str(i+1)+']/div/div/p[4]'
		address=address+' '+driver.find_element_by_xpath(add_xpath).text
		add_xpath='//*[@id="name-search"]/div[5]/div['+str(i+1)+']/div/div/p[5]'
		address=address+' '+driver.find_element_by_xpath(add_xpath).text
		add_xpath='//*[@id="name-search"]/div[5]/div['+str(i+1)+']/div/div/p[6]'
		address=address+' '+driver.find_element_by_xpath(add_xpath).text
		pincode=""
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

		# print(degree)
		tableData=[first_name,last_name,degree,address,pincode,city,'USA',phoneNumber,email,link]
		if(dname not in docterNameArray):
			docterNameArray.append(dname)
			csvwriter = csv.writer(fp)
			csvwriter.writerow(tableData)
		else:
			break
	newlink=""
	if(k<=5):
		newlink=driver.find_element_by_xpath('//*[@id="name-search"]/div[3]/button[11]')
	else:
		newlink=driver.find_element_by_xpath('//*[@id="name-search"]/div[3]/button[12]')
	# //*[@id="name-search"]/div[6]/button[11]
	# //*[@id="name-search"]/div[3]/button[12]

fp.close()


# fp=open("Ishrs-UK.csv","w")
# docterNameArray=[]
# column=['firstname','Lastname','degrees','address','pincode','phoneNumber','city',"country",'email',"link"]
# csvwriter = csv.writer(fp)
# csvwriter.writerow(column)

# docterNameArray=[]
# url="https://ishrs.org/find-a-doctor/"
# p = re.compile(r'^(\s+)?(Mr(\.)?|Mrs(\.)?)?(?P<FIRST_NAME>.+)(\s+)(?P<LAST_NAME>.+)$', re.IGNORECASE)

# driver = webdriver.Chrome(executable_path='chromedriver')
# # data=soup.find_all("div",{"class":"wpb_wrapper"})
# # print(len(data))
# # for content in data:
# # 	newdata=content.find_all("div",{"class":"wpb_text_column wpb_content_element "})
# # 	print(newdata)//*[@id="wpgmza_table_1"]/tbody
# driver.get(url)
# driver.find_element_by_id("name-search-button").click()
# # time.sleep(2)
# driver.find_element_by_xpath("""//*[@id="advanced-search-country"]""").click()
# # time.sleep(2)
# driver.find_element_by_xpath("""//*[@id="advanced-search-country"]/option[232]""").click()
# # time.sleep(2)
# # names=driver.find_element_by_tag_name('h3').find_elements_by_class_name('ng-binding')
# # print(names)
# # time.sleep(2)
# # driver.
# # get_div = driver.find_element_by_css_selector('p')
# # print(get_div.text)
# # //*[@id="name-search"]/div[5]/div[1]/div/div/p[3]
# newlink=driver.find_element_by_xpath('//*[@id="name-search"]/div[3]/span')
# while(newlink!=None):
# 	newlink.click()
# 	print(newlink)
# 	links =driver.find_elements_by_class_name('view-profile')
# 	address=""
# 	for i in range(0,len(links)):
# 		link=links[i].get_attribute("href")
# 		result=requests.get(link)
# 		src = result.content
# 		soup = BeautifulSoup(src, "lxml")
# 		phoneNumber=soup.find('a',{'class':'call-user'}).attrs['href']
# 		email=soup.find('a',{'class':'email-user'}).attrs['data-email']
# 		dname_xpath='//*[@id="name-search"]/div[5]/div['+str(i+1)+']/div/div/a[1]/h3'
# 		dname=driver.find_element_by_xpath(dname_xpath).text
# 		Array=dname.split(',')

# 		m = p.match(Array[0])
# 		first_name=""
# 		last_name=""
# 		if(m != None):
# 			first_name = m.group('FIRST_NAME')
# 			last_name = m.group('LAST_NAME')
# 		if('Dr.' in first_name):
# 			first_name=first_name.replace("Dr.","")
# 		elif('Dr .' in first_name):
# 			first_name=first_name.replace("Dr","")
# 		elif('Dr' in first_name):
# 			first_name=first_name.replace("Dr","")

# 		degree=""
# 		for j in range(1,len(Array)):
# 			degree=degree+Array[j]
# 		# print(first_name,last_name)
# 		phoneNumber=phonenumbers.format_number(phonenumbers.parse(phoneNumber, 'GB'), phonenumbers.PhoneNumberFormat.NATIONAL)
# 		phoneNumber='+44'+phoneNumber[1:len(phoneNumber)]
# 		add_xpath='//*[@id="name-search"]/div[5]/div['+str(i+1)+']/div/div/p[3]'
# 		address=driver.find_element_by_xpath(add_xpath).text
# 		add_xpath='//*[@id="name-search"]/div[5]/div['+str(i+1)+']/div/div/p[4]'
# 		address=address+' '+driver.find_element_by_xpath(add_xpath).text
# 		add_xpath='//*[@id="name-search"]/div[5]/div['+str(i+1)+']/div/div/p[5]'
# 		address=address+' '+driver.find_element_by_xpath(add_xpath).text
# 		add_xpath='//*[@id="name-search"]/div[5]/div['+str(i+1)+']/div/div/p[6]'
# 		address=address+' '+driver.find_element_by_xpath(add_xpath).text
# 		pincode=""
# 		if(address!=None):
# 			zipcode = re.search(r'\d{5}(?:-\d{4})?(?=\D*$)', address)
# 			if(zipcode!=None):
# 				pincode=zipcode.group()
# 			else:
# 				pincode="-"
		
# 		places = GeoText(address)
# 		city=places.cities

# 		print(degree)
# 		tableData=[first_name,last_name,degree,address,pincode,place,'IN',phoneNumber,email,link]		# print(tableData)
# 		if(dname not in docterNameArray):
# 			docterNameArray.append(dname)
# 			csvwriter = csv.writer(fp)
# 			csvwriter.writerow(tableData)
# 		else:
# 			break
# 	newlink=driver.find_element_by_xpath('//*[@id="name-search"]/div[3]/button[11]')
# 	if(newlink==None):
# 		print("End")
# 		break
# fp.close()


# fp=open("Ishrs-UAE.csv","w")
# docterNameArray=[]
# column=['firstname','Lastname','degrees','address','pincode','phoneNumber','city',"country",'email',"link"]
# csvwriter = csv.writer(fp)
# csvwriter.writerow(column)

# docterNameArray=[]
# url="https://ishrs.org/find-a-doctor/"
# p = re.compile(r'^(\s+)?(Mr(\.)?|Mrs(\.)?)?(?P<FIRST_NAME>.+)(\s+)(?P<LAST_NAME>.+)$', re.IGNORECASE)

# driver = webdriver.Chrome(executable_path='chromedriver')
# # data=soup.find_all("div",{"class":"wpb_wrapper"})
# # print(len(data))
# # for content in data:
# # 	newdata=content.find_all("div",{"class":"wpb_text_column wpb_content_element "})
# # 	print(newdata)//*[@id="wpgmza_table_1"]/tbody
# driver.get(url)
# driver.find_element_by_id("name-search-button").click()
# # time.sleep(2)
# driver.find_element_by_xpath("""//*[@id="advanced-search-country"]""").click()
# # time.sleep(2)
# driver.find_element_by_xpath("""//*[@id="advanced-search-country"]/option[231]""").click()
# # time.sleep(2)
# # names=driver.find_element_by_tag_name('h3').find_elements_by_class_name('ng-binding')
# # print(names)
# # time.sleep(2)
# # driver.
# # get_div = driver.find_element_by_css_selector('p')
# # print(get_div.text)
# # //*[@id="name-search"]/div[5]/div[1]/div/div/p[3]
# newlink=driver.find_element_by_xpath('//*[@id="name-search"]/div[3]/span')
# while(newlink!=None):
# 	newlink.click()
# 	print(newlink)
# 	links =driver.find_elements_by_class_name('view-profile')
# 	address=""
# 	for i in range(0,len(links)):
# 		link=links[i].get_attribute("href")
# 		result=requests.get(link)
# 		src = result.content
# 		soup = BeautifulSoup(src, "lxml")
# 		phoneNumber=soup.find('a',{'class':'call-user'}).attrs['href']
# 		email=soup.find('a',{'class':'email-user'}).attrs['data-email']
# 		dname_xpath='//*[@id="name-search"]/div[5]/div['+str(i+1)+']/div/div/a[1]/h3'
# 		dname=driver.find_element_by_xpath(dname_xpath).text
# 		Array=dname.split(',')

# 		m = p.match(Array[0])
# 		first_name=""
# 		last_name=""
# 		if(m != None):
# 			first_name = m.group('FIRST_NAME')
# 			last_name = m.group('LAST_NAME')
# 		if('Dr.' in first_name):
# 			first_name=first_name.replace("Dr.","")
# 		elif('Dr .' in first_name):
# 			first_name=first_name.replace("Dr","")
# 		elif('Dr' in first_name):
# 			first_name=first_name.replace("Dr","")

# 		degree=""
# 		for j in range(1,len(Array)):
# 			degree=degree+Array[j]
# 		# print(first_name,last_name)
# 		phoneNumber=phonenumbers.format_number(phonenumbers.parse(phoneNumber, 'UAE'), phonenumbers.PhoneNumberFormat.NATIONAL)
# 		phoneNumber='+971'+phoneNumber[1:len(phoneNumber)]
# 		add_xpath='//*[@id="name-search"]/div[5]/div['+str(i+1)+']/div/div/p[3]'
# 		address=driver.find_element_by_xpath(add_xpath).text
# 		add_xpath='//*[@id="name-search"]/div[5]/div['+str(i+1)+']/div/div/p[4]'
# 		address=address+' '+driver.find_element_by_xpath(add_xpath).text
# 		add_xpath='//*[@id="name-search"]/div[5]/div['+str(i+1)+']/div/div/p[5]'
# 		address=address+' '+driver.find_element_by_xpath(add_xpath).text
# 		add_xpath='//*[@id="name-search"]/div[5]/div['+str(i+1)+']/div/div/p[6]'
# 		address=address+' '+driver.find_element_by_xpath(add_xpath).text
# 		pincode=""
# 		if(address!=None):
# 			zipcode = re.search(r'\d{5}(?:-\d{4})?(?=\D*$)', address)
# 			if(zipcode!=None):
# 				pincode=zipcode.group()
# 			else:
# 				pincode="-"
		
# 		places = GeoText(address)
# 		city=places.cities

# 		print(degree)
# 		tableData=[first_name,last_name,degree,address,pincode,place,'IN',phoneNumber,email,link]		# print(tableData)
# 		if(dname not in docterNameArray):
# 			docterNameArray.append(dname)
# 			csvwriter = csv.writer(fp)
# 			csvwriter.writerow(tableData)
# 		else:
# 			break

# 	newlink=driver.find_element_by_xpath('//*[@id="name-search"]/div[3]/button[11]')
# 	if(newlink==None):
# 		print("End")
# 		break
	
# fp.close()

# #//*[@id="name-search"]/div[5]/div[1]/div/div/p[2]
# # //*[@id="name-search"]/div[5]/div[1]/div/div/p[3] 
# # //*[@id="name-search"]/div[5]/div[1]/div/div/p[5]
# # driver.
# # country=data.find_element_by_xpath("""//*[@id="advanced-search-country"]""").click()
# # data=driver.find_element_by_xpath("""//*[@id="wpgmza_table_1"]/tbody""")
# # print(data.find_element_by_tag_name('tr'))
# # for i in range(0,91):
# # data=driver.find_element_by_xpath("""//*[@id="wpgmza_table_1"]/tbody""")
# # name=data.find_element_by_class_name('wpgmza_table_title').text
# # address=data.find_element_by_class_name('wpgmza_table_address').text
# # description=data.find_element_by_class_name('wpgmza_table_description').text
# # link=data.find_element_by_tag_name('a').get_attribute("href")
# # print(name,address,description,link)


# # driver.find_element_by_link_text("Next").click() 
# # newData=data.split('\n')
# # csvwriter = csv.writer(fp)
# # csvwriter.writerow(['name','address'])
# # for content in newData:


