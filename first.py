import requests
import sys
import csv
import re
from bs4 import BeautifulSoup
primaryPhoneNumber=[]
SecondaryPhoneNumber=[]
otherPhoneNumber=[]
fp1=open("iapps_phone_number.txt","r")
getPhoneNumber=fp1.readlines()
print(len(getPhoneNumber))
i=0
for phone in getPhoneNumber:
	 newArray=[]
	 flag1=0
	 flag2=0
	 newArray=phone.split(',')
	 if(newArray[0].find('/')>0):
	 	phoneNumber=newArray[0].split('/')
	 	primaryPhoneNumber.append(phoneNumber[0])
	 else:
	 	phoneNumber1=re.sub('[^A-Za-z0-9]+', '', newArray[0])
	 	if(len(phoneNumber1)==10):
	 		primaryPhoneNumber.append(phoneNumber1)
	 	elif(len(phoneNumber1)==12):
	 		primaryPhoneNumber.append(phoneNumber1[2:len(phoneNumber1)])
	 	elif(len(phoneNumber1)==11):
	 		primaryPhoneNumber.append(phoneNumber1[1:len(phoneNumber1)])
	 	else:
	 		flag1=1
	 		primaryPhoneNumber.append('-')

	 if(len(newArray)>1):
	 	 if(newArray[1].find('/')>0):
	 	 	SecondaryPhoneNumber.append("-")
	 	 	flag2=1;
	 	 else:
	 	 	phoneNumber1=re.sub('[^A-Za-z0-9]+', '', newArray[1])
	 	 	if(len(phoneNumber1)==10):
	 	 		SecondaryPhoneNumber.append(phoneNumber1)
	 	 	elif(len(phoneNumber1)==12):
	 	 		SecondaryPhoneNumber.append(phoneNumber1[2:len(phoneNumber1)])
	 	 	elif(len(phoneNumber1)==11):
	 	 		SecondaryPhoneNumber.append(phoneNumber1[1:len(phoneNumber1)])
	 	 	else:
	 	 		flag2=1
	 	 		SecondaryPhoneNumber.append('-')
	 else:
	  	SecondaryPhoneNumber.append("-")


	 if(flag1==1 and flag2==1):
	 	otherPhoneNumber.append(phoneNumber1)
	 else:
	 	if(flag1==1):
	 		otherPhoneNumber.append(newArray[0])
	 	if(flag2==1):
	 		otherPhoneNumber.append(newArray[1])
	 if(flag1==0 and flag2==0):
	 	otherPhoneNumber.append("-")



print(len(primaryPhoneNumber),len(SecondaryPhoneNumber),len(otherPhoneNumber))

cityFilePointer=open("newCity.txt","r")

fp=open("iaaps_new_data.csv","w");
getAllData=[]
mainDoctersName=[]
count=0
mainCount=0
getAllCity=cityFilePointer.readlines();
column=['Name','Country','Sex','Degree','Full Association','state','Date Of Birth','Institution','Life/Annual','E-mail Address','city','Age','Year Of Passing','Reg. Numbers','Address','Memberships / Fellowships/Experience In Aesthetic Plastic Surgery','Primary Phone Number','Secondary Phone Number','other Phone Number']
csvwriter = csv.writer(fp)
csvwriter.writerow(column) 
phoneCount=0
for city in getAllCity:
	url="https://www.iaaps.net/members/?um_search=1&search=&city="+city
	result=requests.get(url)
	src = result.content
	soup = BeautifulSoup(src, "lxml")
	doctersName=[]
	urllist=[]
	print(city)
	outerDivData=soup.find_all("div", {"class":"um-member-name um_member_list_ttl"})
	for content in outerDivData:
		name=content.find("a").text
		doctersName.append(name)
		urllist.append(content.find("a").attrs["href"])


	count=0
	for urlContent in urllist:
		result=requests.get(urlContent)
		src = result.content
		soup = BeautifulSoup(src, "lxml")
		outerDivData=[]
		doctersDataArray=[]
		outerDivData1=soup.find_all("div", {"class":"um-col-131"})
		outerDivData2=soup.find_all("div", {"class":"um-col-132"})
		outerDivData3=soup.find_all("div", {"class":"um-col-133"})
		outerDivData4=soup.find_all("div", {"class":"um-col-1"})

		for content in outerDivData1:
			doctersDataValue=content.find("div",{"class":"um-field-value"})
			if(doctersDataValue!=None ):
				doctersDataArray.append(doctersDataValue.text)
			else:
				doctersDataArray.append("-")


		for i in range(1,len(outerDivData2)): #content in outerDivData2:

			doctersData=outerDivData2[i].find("div",{"class":"um-field-value"})
			if(doctersData!=None):
				doctersDataArray.append(doctersData.text)
			else:
				doctersDataArray.append("-")


		for content in outerDivData3:
			doctersData=content.find("div",{"class":"um-field-value"})
			if(doctersData!=None):
				doctersDataArray.append(doctersData.text)
			else:
				doctersDataArray.append("-")

		for content in outerDivData4:
			doctersData=content.find("div",{"class":"um-field-value"})
			if(doctersData!=None):
				doctersDataArray.append(doctersData.text)
			else:
				doctersDataArray.append("-")


		if(doctersDataArray[0] not in mainDoctersName):
			mainDoctersName.append(doctersDataArray[0])
			doctersDataArray.append(primaryPhoneNumber[phoneCount])
			doctersDataArray.append(SecondaryPhoneNumber[phoneCount])
			doctersDataArray.append(otherPhoneNumber[phoneCount])	
			csvwriter = csv.writer(fp)
			csvwriter.writerow(doctersDataArray)
			count=count+1
			phoneCount=phoneCount+1
			


		else:
			print(doctersDataArray[0])
		
	mainCount=mainCount+count

	


print("Total")
print(mainCount)
	


	

	





	
	