import requests
import csv
from bs4 import BeautifulSoup

fileName="IAAPS.csv"
fp=open(fileName,"w");
url="https://www.iaaps.net/members/?um_search=1&search=&city=delhi"
result=requests.get(url)
src = result.content
soup = BeautifulSoup(src, "lxml")
doctersName=[]
urllist=[]

outerDivData=soup.find_all("div", {"class":"um-member-name um_member_list_ttl"})
for content in outerDivData:
	name=content.find("a").text
	doctersName.append(name)
	urllist.append(content.find("a").attrs["href"])

column=['Name','Country','Sex','Degree','Full Association','Phone No','state','Date Of Birth','Institution','Life/Annual','E-mail Address','city','Age','Year Of Passing','Reg. Numbers','Address','Memberships / Fellowships/Experience In Aesthetic Plastic Surgery']
csvwriter = csv.writer(fp)
csvwriter.writerow(column)

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
	print("******************")

	for content in outerDivData1:
		doctersDataValue=content.find("div",{"class":"um-field-value"})
		if(doctersDataValue!=None ):
			doctersDataArray.append(doctersDataValue.text)
		else:
			doctersDataArray.append("-")


	for content in outerDivData2:
		doctersData=content.find("div",{"class":"um-field-value"})
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

	print(doctersDataArray)
	count=count+1
	csvwriter = csv.writer(fp)
	csvwriter.writerow(doctersDataArray)

print(count)
	

	





	
	