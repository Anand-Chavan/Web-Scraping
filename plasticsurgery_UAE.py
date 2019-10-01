
import requests
import sys
import csv
import re
from bs4 import BeautifulSoup
docterNameArray=[]
i=1
# fp=open("Plastic_Surgery_India.csv","w")
# url="https://find.plasticsurgery.org/country/india/?page=1"
fp=open("Plastic_Surgery_UAE.csv","w")

csvwriter = csv.writer(fp)
csvwriter.writerow(['Firstname','Lastname','degree','address','pincode','telephone'])
# print(len(data))
p = re.compile(r'^(\s+)?(Mr(\.)?|Mrs(\.)?)?(?P<FIRST_NAME>.+)(\s+)(?P<LAST_NAME>.+)$', re.IGNORECASE)

k=0
for k in range(0,5):

	url="https://find.plasticsurgery.org/?q=United%2BArab%2BAmirati&page=1"
	# print(url)
	result=requests.get(url)
	src = result.content
	soup = BeautifulSoup(src, "lxml")
	data=soup.find_all("div",{"class":"resultSet col-md-6 col-xs-12"})
	def getPlasticSurgeryData(data):
		for city in data:
			value=city.find_all("div",{"class":"col-xs-12"})
			for content in value:
				docterName=content.find("span",{"itemprop":"givenName"}).text
				address=content.find("p",{"itemprop":"address"}).text
				address=' '.join(address.split())
				telephone=re.sub('[^A-Za-z0-9]+', '',content.find("p",{"itemprop":"telephone"}).text)
				if(len(telephone)==12):
					telephone=telephone[2:len(telephone)]
				if(len(telephone)==13):
					telephone=telephone[2:len(telephone)]
				if(len(telephone)==14):
					telephone=telephone[2:len(telephone)]

				data=docterName.split(",")
				m = p.match(data[0])
				if(m != None):
					first_name = m.group('FIRST_NAME')
					last_name = m.group('LAST_NAME')
				degree=data[1]

				if(address!=None):
					zipcode = re.search(r'\d{6}(?:-\d{4})?(?=\D*$)', address)
					if(zipcode!=None):
						pincode=zipcode.group()
					else:
						pincode="-"
			
				if(len(telephone)>8):
					print(telephone)
					telephone='+'+telephone

				elif(len(telephone)<=8):
					telephone='+971'+telephone
				

			
				if(docterName not in docterNameArray):
					docterNameArray.append(docterName)
					csvwriter = csv.writer(fp)
					csvwriter.writerow([first_name,last_name,degree,address,pincode,telephone])
				

	getPlasticSurgeryData(data)
	i=1
	nextPageData=soup.find("div",{"class":"col-xs-12 results-pager"})
	while(nextPageData.find("a",{"rel":"next"}).has_attr('href')):
		i=i+1
		url="https://find.plasticsurgery.org/?q=United%2BArab%2BAmirati&page="+str(i)
		# print(url)
		result=requests.get(url)
		src = result.content
		soup = BeautifulSoup(src, "lxml")
		data=soup.find_all("div",{"class":"resultSet col-md-6 col-xs-12"})
		getPlasticSurgeryData(data)
		nextPageData=soup.find("div",{"class":"col-xs-12 results-pager"})

print(len(docterNameArray))