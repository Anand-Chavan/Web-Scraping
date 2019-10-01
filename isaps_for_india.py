import requests
import csv
import re
from bs4 import BeautifulSoup
from geotext import GeoText
fileName="ISAPS-INDIA.csv"
fp=open(fileName,"w")
column=['first_name','last_name','degree','memberType','address','pincode','phoneNumber','faxNumber','emailId','IN','city']
p = re.compile(r'^(\s+)?(Mr(\.)?|Mrs(\.)?)?(?P<FIRST_NAME>.+)(\s+)(?P<LAST_NAME>.+)$', re.IGNORECASE)
csvwriter = csv.writer(fp)
csvwriter.writerow(column)
country="india"
docterNameArray=[]
cityFilePointer=open("newCity.txt","r")
getAllCity=cityFilePointer.readlines();
for city in getAllCity:
	print(city)
	url="https://www.isaps.org/listings/?searchtype=statecountry&country="+country+"&state=&city="+city
	result=requests.get(url)
	src = result.content
	soup = BeautifulSoup(src, "lxml")
	dataForScrap=soup.find_all("a",{"class":"page-numbers"})
	InitialData=soup.find_all("div",{"class":"amdoctor col-lg-6 col-md-6 col-sm-6 col-xs-12"})

	def setDataForISAPS(InitialData):
		for content in InitialData:
			docterName=content.find("h2").text
			name=docterName
			memberType=content.find("span").text
			address=content.find("address").text
			spanData=content.find("address").find_all("span",{"class":"block"})
			emailId=""
			phoneNumber=""
			faxNumber=""
			if('Dr.' in docterName):
				docterName=docterName.replace("Dr.","")
			elif('Dr .' in docterName):
				docterName=docterName.replace("Dr","")
			elif('Dr' in docterName):
				docterName=docterName.replace("Dr","")

			split1=docterName.split(',')
			split2=split1[0].split(' ')
			first_name=split2[1]
			last_name=split2[len(split2)-2]
			degree=""
			degree=split2[len(split2)-1]
			for k in range(1,len(split1)):
				degree=degree+''+split1[k]
			# print(degree)
			
			for value in spanData:
				findOtherData=value.text;
				if(findOtherData.find("t:")!=-1):
					phoneNumber=findOtherData
				
				if(findOtherData.find("f:")!=-1):
					faxNumber=findOtherData

				if(findOtherData.find("www.")!=-1):
					emailId=findOtherData

		


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

			phoneNumber=re.sub('[^0-9]+', '',phoneNumber)
			if(len(phoneNumber)<=10 and len(phoneNumber)>=5):
				phoneNumber='+91'+phoneNumber
			elif(len(phoneNumber)==12):
				phoneNumber='+'+phoneNumber


	
			print(phoneNumber)
			# print(first_name,last_name)
			if(name not in docterNameArray):
				docterNameArray.append(name)
				csvwriter = csv.writer(fp)
				csvwriter.writerow([first_name,last_name,degree,memberType,address,pincode,phoneNumber,faxNumber,emailId,'IN',place])

	setDataForISAPS(InitialData)

	for content in dataForScrap:
		url=content.attrs["href"]
		result=requests.get(url)
		src = result.content
		soup = BeautifulSoup(src, "lxml")
		InitialData=soup.find_all("div",{"class":"amdoctor col-lg-6 col-md-6 col-sm-6 col-xs-12"})
		setDataForISAPS(InitialData)


	


	

