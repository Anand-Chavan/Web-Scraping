import requests
import sys
import csv
import re
import time
from bs4 import BeautifulSoup
docterNameArray=[]
i=1
fp=open("Plastic_Surgery_USA.csv","w")
url="https://find.plasticsurgery.org/country/united%20states/?page=1"
result=requests.get(url)
src = result.content
soup = BeautifulSoup(src, "lxml")
data=soup.find_all("div",{"class":"resultSet col-md-6 col-xs-12"})
csvwriter = csv.writer(fp)
csvwriter.writerow(['docterName','address','telephone'])
# print(len(data))
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
			if(docterName not in docterNameArray):
				docterNameArray.append(docterName)
				csvwriter = csv.writer(fp)
				csvwriter.writerow([docterName,address,telephone])
			

getPlasticSurgeryData(data)

nextPageData=soup.find("div",{"class":"col-xs-12 results-pager"})
while(nextPageData.find("a",{"rel":"next"}).has_attr('href')):
	i=i+1

	url="https://find.plasticsurgery.org/country/united%20states/?page="+str(i)

	print(url)
	result=requests.get(url)
	time.sleep(1)
	src = result.content
	soup = BeautifulSoup(src, "lxml")
	data=soup.find_all("div",{"class":"resultSet col-md-6 col-xs-12"})
	getPlasticSurgeryData(data)
	nextPageData=soup.find("div",{"class":"col-xs-12 results-pager"})
