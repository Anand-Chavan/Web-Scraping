import csv 
import re
from geotext import GeoText
p = re.compile(r'^(\s+)?(Mr(\.)?|Mrs(\.)?)?(?P<FIRST_NAME>.+)(\s+)(?P<LAST_NAME>.+)$', re.IGNORECASE)

fp=open("ISAPS-India.csv","r")	
# firstname	Lastname	degrees	memberType	address	Phone No with CC	phoneNumber	faxNumber	Website	city
fp2=open("IS-Indis.csv","w")
# column=['firstname','Lastname','degrees','memberType','address','pincode','phoneNumber','faxNumber','Website','city','country']
# csvwriter = csv.writer(fp2)
# csvwriter.writerow(column)
# country="IN"

line=fp.readlines()
for i in range(1,len(line)):
	data=line[i].split(',')
	# places = GeoText(data[9])
	# city=places.cities
	# print(city)
	# address=data[5].split(':')
	print(data[0])


	# pincode=""
	# if(address!=None):
	# 	zipcode = re.search(r'\d{6}(?:-\d{4})?(?=\D*$)', address)
	# if(zipcode!=None):
	# 	pincode=zipcode.group()
	# else:
	# 	pincode="-"
	# tableData=[data[0],data[1],data[2],data[3],address,data[5],data[6],data[7],data[8],data[9],data[10]]
	# # print(tableData)
	# csvwriter = csv.writer(fp2)
	# csvwriter.writerow(tableData)



# fp.close()
# fp2.close()
# # firstname	Lastname	degrees	memberType	address	phoneNumber	faxNumber	Website	city
# fp=open("ISAPS-UAE.csv","r")	
# fp2=open("IS-UAE.csv","w")
# column=['firstname','Lastname','degrees','memberType','address','pincode','phoneNumber','faxNumber','Website','city','country']
# csvwriter = csv.writer(fp2)
# csvwriter.writerow(column)
# country="UAE"
# line=fp.readlines()
# for i in range(1,len(line)):
# 	data=line[i].split('\t')
# 	# places = GeoText(data[9])
# 	# city=places.cities
# 	# print(city)
# 	address=data[4]
# 	pincode=""
# 	if(address!=None):
# 		zipcode = re.search(r'\d{6}(?:-\d{4})?(?=\D*$)', address)
# 	if(zipcode!=None):
# 		pincode=zipcode.group()
# 	else:
# 		pincode="-"
# 	telephone=data[5]
# 	if(len(telephone)>=8):
# 		telephone='+971'+telephone
# 	else:
# 		telephone=""
# 	tableData=[data[0],data[1],data[2],data[3],data[4],pincode,telephone,data[6],data[7],data[8],country]
# 	# print(tableData)
# 	csvwriter = csv.writer(fp2)
# 	csvwriter.writerow(tableData)


# fp.close()
# fp2.close()
# # firstname	Lastname	degrees	memberType	address	phoneNumber	faxNumber	Website	city
# fp=open("ISAPS-UK.csv","r")	
# fp2=open("IS-UK.csv","w")
# column=['firstname','Lastname','degrees','memberType','address','pincode','phoneNumber','faxNumber','Website','city','country']
# csvwriter = csv.writer(fp2)
# csvwriter.writerow(column)
# country="GB"
# line=fp.readlines()
# for i in range(1,len(line)):
# 	data=line[i].split('\t')
# 	# places = GeoText(data[9])
# 	# city=places.cities
# 	# print(city)
# 	address=data[4]
# 	pincode=""
# 	if(address!=None):
# 		zipcode = re.search(r'\d{6}(?:-\d{4})?(?=\D*$)', address)
# 	if(zipcode!=None):
# 		pincode=zipcode.group()
# 	else:
# 		pincode="-"
# 	telephone=data[5]
# 	if(len(telephone)>=10):
# 		telephone='+44'+telephone
# 	else:
# 		telephone=""
# 	tableData=[data[0],data[1],data[2],data[3],data[4],pincode,telephone,data[6],data[7],data[8],country]
# 	# print(tableData)
# 	csvwriter = csv.writer(fp2)
# 	csvwriter.writerow(tableData)


# fp.close()
# fp2.close()
# # firstname	Lastname	degrees	memberType	address	phoneNumber	faxNumber	Website	city
# fp=open("ISAPS-USA.csv","r")	
# fp2=open("IS-USA.csv","w")
# column=['firstname','Lastname','degrees','memberType','address','pincode','phoneNumber','faxNumber','Website','city',"country"]
# csvwriter = csv.writer(fp2)
# csvwriter.writerow(column)
# country="USA"
# line=fp.readlines()
# for i in range(1,len(line)):
# 	data=line[i].split('\t')
# 	# places = GeoText(data[9])
# 	# city=places.cities
# 	# print(city)
# 	address=data[4]
# 	pincode=""
# 	if(address!=None):
# 		zipcode = re.search(r'\d{6}(?:-\d{4})?(?=\D*$)', address)
# 	if(zipcode!=None):
# 		pincode=zipcode.group()
# 	else:
# 		pincode="-"
# 	telephone=data[5]
# 	if(len(telephone)>=10):
# 		telephone='+1'+telephone
# 	else:
# 		telephone=""
# 	tableData=[data[0],data[1],data[2],data[3],data[4],pincode,telephone,data[6],data[7],data[8],country]
# 	print(tableData)
# 	csvwriter = csv.writer(fp2)
# 	csvwriter.writerow(tableData)