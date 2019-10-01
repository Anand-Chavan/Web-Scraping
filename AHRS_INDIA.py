import sys
import requests
import csv
from bs4 import BeautifulSoup
import re
# from googlemaps import Client as GoogleMaps
import phonenumbers

fp=open("AHRS-INDIA.csv","w")
url="https://www.ahrsindia.org/member-section"
result=requests.get(url)
src = result.content
soup = BeautifulSoup(src, "lxml")
doctersData=[]
doctersName=[]
firstPageData=soup.find_all("tbody",{"id":"userData"})
newTableData=firstPageData[0].find_all("tr")

p = re.compile(r'^(\s+)?(Mr(\.)?|Mrs(\.)?)?(?P<FIRST_NAME>.+)(\s+)(?P<LAST_NAME>.+)$', re.IGNORECASE)

column=['Sno','Membership No','first_name','last_name','Category Of Member','Membership Year','Clinic Name','Address','Pin Code','City','State','Email','Degree','Website','Primary Number','Secondary Number','Other Number']
csvwriter = csv.writer(fp)
csvwriter.writerow(column)
i=0

for content in newTableData:
	findTd=content.find_all("td")
	newArray=[]
	csvArray=[]
	for data in findTd:
		newArray.append(data.text)
	csvArray.append(newArray[0])
	csvArray.append(newArray[1])
	m = p.match(newArray[2])
	if(m != None):
		first_name = m.group('FIRST_NAME')
		last_name = m.group('LAST_NAME')
	if('Dr.' in first_name):
			first_name=first_name.replace("Dr.","")
	elif('Dr' in first_name):
			first_name=first_name.replace("Dr","")
	elif('DR .' in first_name):
			first_name=first_name.replace("DR .","")
	elif('DR.' in first_name):
			first_name=first_name.replace("DR.","")
	elif('DR' in first_name):
			first_name=first_name.replace("DR","")




	csvArray.append(first_name)
	csvArray.append(last_name)
	csvArray.append(newArray[3])
	csvArray.append(newArray[4])
	csvArray.append(newArray[5])
	csvArray.append(newArray[6])
	pincode=""
	if(newArray[6]!=None):
		zipcode = re.search(r'\d{6}(?:-\d{4})?(?=\D*$)', newArray[6])
		if(zipcode!=None):
			pincode=zipcode.group()
	else:
		pincode="-"
	csvArray.append(pincode)
	csvArray.append(newArray[7])
	csvArray.append(newArray[8])
	# csvArray.append(newArray[9])
	phoneNumber=[]
	telephone=[]
	if('/' in newArray[9]):
		phoneNumber=newArray[9].split("/")
	elif('.' in newArray[9]):
		phoneNumber=newArray[9].split(".")
	elif(',' in newArray[9]):
		phoneNumber=newArray[9].split(",")
	else:
		phoneNumber=newArray[9].split(" ")

	for numbers in phoneNumber:
		tel=re.sub('[^0-9]+', '',numbers)
		telephone.append(''.join(i for i in tel if i.isdigit()))
	i=i+1
	newPhoneNumbers=[]
	tel=""
	
	
	if('' not in telephone):
		if(len(telephone)<=3):
			tel=""
			flag=0
			for data in telephone:
				if(len(data)>=10):
					tel=phonenumbers.format_number(phonenumbers.parse(data, 'IN'),'IN')
					newPhoneNumbers.append('+91'+tel[0:len(tel)])
				else:
					tel=tel+data
					flag=1
			if(flag):
				tel=phonenumbers.format_number(phonenumbers.parse(tel, 'IN'),'IN')
				newPhoneNumbers.append('+91'+tel[0:len(tel)])


		else:
			tel=""
			for data in telephone:
				tel=tel+data
			tel=phonenumbers.format_number(phonenumbers.parse(tel, 'IN'),'IN')
			newPhoneNumbers.append('+91'+tel[0:len(tel)])


	csvArray.append(newArray[10])
	csvArray.append(newArray[11])
	csvArray.append(newArray[12])

	if(len(newPhoneNumbers)==1):
		csvArray.append(newPhoneNumbers[0])
		csvArray.append('-')
		csvArray.append('-')
	elif(len(newPhoneNumbers)==2):
		csvArray.append(newPhoneNumbers[0])
		csvArray.append(newPhoneNumbers[1])
		csvArray.append('-')
	elif(len(newPhoneNumbers)==3):
		csvArray.append(newPhoneNumbers[0])
		csvArray.append(newPhoneNumbers[1])
		csvArray.append(newPhoneNumbers[2])
	else:
		csvArray.append('-')
		csvArray.append('-')
		csvArray.append('-')

	
	print(len(csvArray))

	if(newArray[2] not in doctersName):
		csvwriter = csv.writer(fp)
		csvwriter.writerow(csvArray)
		doctersName.append(newArray[2])
	else:
		print(newArray[2])



