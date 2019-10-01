import requests
import csv
from bs4 import BeautifulSoup
from geotext import GeoText
import re

fileName="ISAPS-UAE.csv"
i=0
fp=open(fileName,"w")
url="https://www.isaps.org/listings/?searchtype=statecountry&country=United%20Arab%20Emirates"
result=requests.get(url)
src = result.content
soup = BeautifulSoup(src, "lxml")
column=['docterName','memberType','address','phoneNumber','faxNumber','Website','city']
dataForScrap=soup.find_all("a",{"class":"next page-numbers"})
InitialData=soup.find_all("div",{"class":"amdoctor col-lg-6 col-md-6 col-sm-6 col-xs-12"})
csvwriter = csv.writer(fp)
csvwriter.writerow(column)
docterNameCollection=[]




def setDataForISAPS(InitialData):
	for content in InitialData:
		docterName=content.find("h2").text
		memberType=content.find("span").text
		address=content.find("address").text
		spanData=content.find("address").find_all("span",{"class":"block"})
		places = GeoText(address)
		emailId=""
		phoneNumber=""
		newPhoneNumber=""
		faxNumber=""
		for value in spanData:
			findOtherData=value.text;
			if(findOtherData.find("t:")!=-1):
				phoneNumber=findOtherData
				array=phoneNumber.split(":")
				newPhoneNumber=re.sub('[^A-Za-z0-9]+', '', array[1])
				newPhoneNumber=newPhoneNumber[3:len(phoneNumber)-1]
				# if(len(newPhoneNumber)==12):
				# 	newPhoneNumber=newPhoneNumber[3:len(phoneNumber)-1]
				# if(len(newPhoneNumber)==13):
				# 	newPhoneNumber=newPhoneNumber[3:len(phoneNumber)-1]
				# if(len(newPhoneNumber)==14):
				# 	newPhoneNumber=newPhoneNumber[4:len(phoneNumber)-1]
				print(newPhoneNumber)
	

				# # print(array)
				# if(array[2].find('/')>0):
				# 	newArray=array[2].split("/")
				# 	newPhoneNumber=re.sub('[^A-Za-z0-9]+', '', newArray[0])
				# else:
				# 	newPhoneNumber=re.sub('[^A-Za-z0-9]+', '', array[2])
				# print("-----")
				# print(newPhoneNumber)
				# if(len(newPhoneNumber)==12):
				# 	newPhoneNumber=newPhoneNumber[2:len(phoneNumber)-1]
				# 	print(newPhoneNumber,len(newPhoneNumber))
					
				# if(len(newPhoneNumber)==13):
				# 	newPhoneNumber=newPhoneNumber[3:len(phoneNumber)-1]

				# # if(newPhoneNumber[0]=='1'):
				# # 	newPhoneNumber=newPhoneNumber[1:len(phoneNumber)-1]
				
			
			if(findOtherData.find("f:")!=-1):
				faxNumber=findOtherData

			if(findOtherData.find("www.")!=-1):
				emailId=findOtherData
		
		# print(docterName,memberType,address,spanData,phoneNumber,faxNumber,emailId)
		if(docterName not in docterNameCollection):
			csvwriter = csv.writer(fp)
			if(places.cities!=[]):
				csvwriter.writerow([docterName,memberType,address,newPhoneNumber,faxNumber,emailId,places.cities[0]])
			else:
				csvwriter.writerow([docterName,memberType,address,newPhoneNumber,faxNumber,emailId,'-'])
			docterNameCollection.append(docterName)
		else:
			print(docterName)

setDataForISAPS(InitialData)

while(dataForScrap!=[]):
	for content in dataForScrap:
		url=content.attrs["href"]
		result=requests.get(url)
		src = result.content
		soup = BeautifulSoup(src, "lxml")
		InitialData=soup.find_all("div",{"class":"amdoctor col-lg-6 col-md-6 col-sm-6 col-xs-12"})
		setDataForISAPS(InitialData)
	dataForScrap=soup.find_all("a",{"class":"next page-numbers"})





print(len(docterNameCollection))


	


	
