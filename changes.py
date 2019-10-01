import re
import csv
fp=open("International Society of Hair Restoration Surgery UAE.csv","r")
fp2=open("New.csv","w")
column=['firstname','Lastname','degrees','address','pincode','city','country','phoneNumber','email','link']
csvwriter = csv.writer(fp2)
csvwriter.writerow(column)
line=fp.readlines()
for data in line:
	splitData=data.split(',')
	address=splitData[3]
	pincode=""
	if(address!=None):
		zipcode = re.search(r'\d{5}(?:-\d{4})?(?=\D*$)', address)
		if(zipcode!=None):
			pincode=zipcode.group()
		else:
			pincode="-"

	phone='+'+splitData[7]
	if(len(phone)>10):
		phoneNumber=phone
	else:
		phoneNumber=""

	csvwriter = csv.writer(fp2)
	csvwriter.writerow([splitData[0],splitData[1],splitData[2],splitData[3],pincode,splitData[5],splitData[6],phoneNumber,splitData[8],splitData[9]])
	
