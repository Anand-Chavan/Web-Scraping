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
fp=open("apsi.csv","w")
column=['firstname','lastname','city','state','country','email','phoneNumber','address','pincode']
csvwriter = csv.writer(fp)
csvwriter.writerow(['firstname','lastname','city','state','country','email','phoneNumber','address','pincode'])

url="http://apsi.in/surgeon-search-result.php"
driver = webdriver.Chrome(executable_path='chromedriver')
driver.get(url)
driver.find_element_by_xpath('//*[@id="usercntry"]').click()
driver.find_element_by_xpath('//*[@id="usercntry"]/option[2]').click()


for k in range(3,4):
	try:
		time.sleep(3)
		string='//*[@id="userstate"]/option['+str(k)+']'
		# //*[@id="city"]/option[2]
		driver.find_element_by_xpath('//*[@id="userstate"]').click()
		driver.find_element_by_xpath(string).click()

	except:
		print()
	for m in range(12,30):
		try:
			time.sleep(4)
			driver.find_element_by_xpath('//*[@id="city"]').click()
			time.sleep(2)
			string4='//*[@id="city"]/option['+str(m)+']'
			# //*[@id="city"]/option[2]
			driver.find_element_by_xpath(string4).click()
			# print(string4)
			time.sleep(2)
			driver.find_element_by_xpath('//*[@id="searchfrm"]/div[5]/button').click()
			time.sleep(2)
			for i in range(2,100):
				dname="-"
				city="-"
				state="-"
				country="-"
				email="-"
				address="-"
				phonenumber="-"
				try:
					string1='//*[@id="memberslistshow"]/div['+str(i)+']/div/div/button'
					data=driver.find_element_by_xpath(string1).click()
					time.sleep(2)
					string2='//*[@id="memberslistshow"]/section['+str(i)+']'
					getsection=driver.find_element_by_xpath(string2)
					getid=getsection.find_element_by_tag_name('div').get_attribute('id')
					dname=driver.find_element_by_xpath('//*[@id="'+str(getid)+'"]/div/div/div[2]/div/div[1]/div[2]/span').text
					city=driver.find_element_by_xpath('//*[@id="'+str(getid)+'"]/div/div/div[2]/div/div[2]/table/tbody/tr[1]/td[2]').text
					state=driver.find_element_by_xpath('//*[@id="'+str(getid)+'"]/div/div/div[2]/div/div[2]/table/tbody/tr[2]/td[2]').text
					country=driver.find_element_by_xpath('//*[@id="'+str(getid)+'"]/div/div/div[2]/div/div[2]/table/tbody/tr[3]/td[2]').text

					try:
						email=driver.find_element_by_xpath('//*[@id="'+str(getid)+'"]/div/div/div[2]/div/div[2]/table/tbody/tr[4]/td[2]').text
					except:
						email="-"

					try:
						address=driver.find_element_by_xpath('//*[@id="'+str(getid)+'"]/div/div/div[2]/div/div[2]/table/tbody/tr[5]/td[2]').text
					except:
						address="-"

					try:
						phonenumber=driver.find_element_by_xpath('//*[@id="'+str(getid)+'"]/div/div/div[2]/div/div[2]/table/tbody/tr[6]/td[2]').text
					except:
						phonenumber="-"

					if('@' not in email):
						address=email
						email="-"

					if(email.isdigit()):
						phonenumber=email

					if(address.isdigit()):
						phonenumber=address



					pincode=""
					reg = re.compile('^.*(?P<zipcode>\d{6}).*$')
					match = reg.match(address)
					if(match):
						pincode=match.groupdict()['zipcode']
					else:
						pincode="-"




					if("-" not in phonenumber):
						phoneNumber=re.sub('[^0-9]+', '',phonenumber)
						if(len(phoneNumber)<=10 and len(phoneNumber)>=5):
							phoneNumber='+91'+phoneNumber
						elif(len(phoneNumber)==12):
							phoneNumber='+'+phoneNumber

			

					firstname=""
					lastname=""
					if('Dr.' in dname):
						dname=dname.replace("Dr.","")
					elif('Dr .' in dname):
						dname=dname.replace("Dr","")
					elif('Dr' in dname):
						dname=dname.replace("Dr","")
					elif('DR .' in dname):
						dname=dname.replace('DR .',"")	
					elif('DR' in dname):
						dname=dname.replace('DR',"")

					if(',' in dname):
						splitDname=dname.split(',')
						firstname=splitDname[1]
						lastname=splitDname[0]
					else:
						splitDname=dname.split(' ')
						firstname=splitDname[0]
						lastname=splitDname[1]

					



					column=[firstname,lastname,city,state,country,email,phoneNumber,address,pincode]
					csvwriter = csv.writer(fp)
					csvwriter.writerow([firstname,lastname,city,state,country,email,phoneNumber,address,pincode])

					print(firstname,lastname)


				except:
					print("")

				finally:
					getid='"'+getid+'"'
					close='//*[@id='+str(getid)+']/div/div/div[1]/button'
					time.sleep(2)
					check=driver.find_element_by_xpath(close).click()
					time.sleep(2)

					
					
		except:
			print("out")
