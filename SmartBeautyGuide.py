import sys
import requests
import csv
from bs4 import BeautifulSoup
import phonenumbers
import re
fp=open("Smartbeautyguide-uk.csv","w")
docterNameArray=[]
url="https://www.smartbeautyguide.com/select-surgeon/?location=uk&search-type=surgeon-locator&search=uk"
result=requests.get(url)
src = result.content
soup = BeautifulSoup(src, "lxml")
firstPageData=soup.find_all("div",{"class":"highlight-items member-items"})
data=firstPageData[0].find_all("div",{"class":"row item"})
print("Hello")
csvwriter = csv.writer(fp)
csvwriter.writerow(['first_name','last_name','degree','phoneNumber','address','pincode','memberType','website'])
p = re.compile(r'^(\s+)?(Mr(\.)?|Mrs(\.)?)?(?P<FIRST_NAME>.+)(\s+)(?P<LAST_NAME>.+)$', re.IGNORECASE)


def getAllPageData(data):
	for content in data:
		docterName=content.find("span",{"class":"fn"}).text
		address=content.find("p").text
		memberType=content.find("div",{"class":"member-status hidden-xs"}).text
		memberType=' '.join(memberType.split())
		phoneNumber=content.find("div",{"class":"reveal-hidden"}).text
		m = p.match(docterName)
		data=docterName.split(",")
		degree=""
		m = p.match(data[0])
		if(m != None):
			first_name = m.group('FIRST_NAME')
			last_name = m.group('LAST_NAME')
		if(len(data)>1):
			degree=data[1]


		pincode=""
		if(address!=None):
			zipcode = re.search(r'\d{6}(?:-\d{4})?(?=\D*$)',address)
			if(zipcode!=None):
				pincode=zipcode.group()
		else:
			pincode="-"

		if(content.find("a").has_attr('href')):
			website=content.find("a").attrs["href"]
			website="https://www.smartbeautyguide.com"+website
		else:
			website="-"
		tel=phonenumbers.format_number(phonenumbers.parse(phoneNumber, 'GB'),'GB')
		tel='+44'+tel
		print(first_name,last_name)		
		if(docterName not in docterNameArray):
			docterNameArray.append(docterName)
			csvwriter = csv.writer(fp)
			csvwriter.writerow([first_name,last_name,degree,tel,address,pincode,memberType,website])
		else:
			print(docterName)

getAllPageData(data)
data=firstPageData[0].find_all("div",{"class":"row item"})
getAllPageData(data)
data=firstPageData[0].find_all("div",{"class":"row item first featured"})
getAllPageData(data)
data=firstPageData[0].find_all("div",{"class":"row item featured"})
getAllPageData(data)
data=firstPageData[0].find_all("div",{"class":"row item last"})
getAllPageData(data)
data=firstPageData[0].find_all("div",{"class":"row item first"})
getAllPageData(data)

pagination=soup.find("li",{"class":"pager-next pager-iteration"}).find("a")

while(pagination!=None):
	url="https://www.smartbeautyguide.com"+pagination.attrs["href"]
	print(url)
	result=requests.get(url)
	src = result.content
	soup = BeautifulSoup(src, "lxml")
	firstPageData=soup.find_all("div",{"class":"highlight-items member-items"})
	data=firstPageData[0].find_all("div",{"class":"row item"})
	getAllPageData(data)
	data=firstPageData[0].find_all("div",{"class":"row item first featured"})
	getAllPageData(data)
	data=firstPageData[0].find_all("div",{"class":"row item featured"})
	getAllPageData(data)
	data=firstPageData[0].find_all("div",{"class":"row item last"})
	getAllPageData(data)
	data=firstPageData[0].find_all("div",{"class":"row item first"})
	getAllPageData(data)
	pagination=soup.find("li",{"class":"pager-next pager-iteration"})
	if(pagination!=None):
		pagination=pagination.find("a")
	else:
		break
	

print(len(docterNameArray))
	


