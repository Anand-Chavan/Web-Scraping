import csv 
import re
import datetime
fp=open("iaaps_new_data.csv","r")
# line=fp.readlines()
# for data in line:
p = re.compile(r'^(\s+)?(Mr(\.)?|Mrs(\.)?)?(?P<FIRST_NAME>.+)(\s+)(?P<LAST_NAME>.+)$', re.IGNORECASE)

fp2=open("Iaaps-India.csv","w")	
column=['firstname','lastname','Country','Sex','Degree','Full Association','state','Date Of Birth','Institution','Life/Annual','E-mail Address','city','Age','Year Of Passing','Reg. Numbers','Address','pincode','Memberships / Fellowships/Experience In Aesthetic Plastic Surgery','Primary Phone Number','Secondary Phone Number','other Phone Number']
csvwriter = csv.writer(fp2)
csvwriter.writerow(column)
# print(len(column))

with fp as csv_file:
    csv_reader = csv.reader(csv_file)
    print(csv_reader)
    for row in csv_reader:
    	m = p.match(row[0])
    	first_name=""
    	last_name=""
    	if(m != None):
    		first_name = m.group('FIRST_NAME')
    		last_name = m.group('LAST_NAME')
    	if('Dr.' in first_name):
    		first_name=first_name.replace("Dr.","")
    	elif('Dr .' in first_name):
    		first_name=first_name.replace("Dr","")
    	elif('Dr' in first_name):
    		first_name=first_name.replace("Dr","")

    

    	address=row[14]
    	pincode=""
    	if(address!=None):
    		zipcode = re.search(r'\d{5}(?:-\d{4})?(?=\D*$)', address)
    		if(zipcode!=None):
    			pincode=zipcode.group()
    		else:
    			pincode="-"
    	telephone1=row[16]
    	if(len(telephone1)>=10):
    		telephone1='+91'+telephone1

    	telephone2=row[17]
    	if(len(telephone2)>=10):
    		telephone2='+91'+telephone2
  

    	gender=""
    	if(row[2]=="Female" or row[2]=="female" or "Female" in row[2]):
    		gender="F"

    	if(row[2]=="Male" or row[2]=="male" or "Male" in row[2]):
    		gender="M"

    	tableData=[first_name,last_name,row[1],gender,row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],address,pincode,row[15],telephone1,telephone2,row[18]]
    	# print(len(tableData))
    	csvwriter = csv.writer(fp2)
    	csvwriter.writerow(tableData)



    	
