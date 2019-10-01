import csv 
import re
import datetime
from geotext import GeoText
import phonenumbers
fp=open("American Society of Plastic Surgeons-UAE.csv","r")
# line=fp.readlines()
# for data in line:
p = re.compile(r'^(\s+)?(Mr(\.)?|Mrs(\.)?)?(?P<FIRST_NAME>.+)(\s+)(?P<LAST_NAME>.+)$', re.IGNORECASE)

fp2=open("American Society of Plastic Surgeons-UAE-New.csv","w")	
column=['Firstname','Lastname','degree','address','pincode','city','country','telephone']
csvwriter = csv.writer(fp2)
csvwriter.writerow(column)
# print(len(column))

with fp as csv_file:
    csv_reader = csv.reader(csv_file)
    print(csv_reader)
    for row in csv_reader:
        address=row[3]
        places = GeoText(address)
        city=places.cities
        place=""
        if(city!=[]):
            place=city[0]

        phoneNumber=re.sub('[^0-9]+', '',row[3])
        if(len(phoneNumber)>=3):
            phoneNumber='+971'+phoneNumber
        else:
            phoneNumber=""
        tableData=[row[0],row[1],row[2],row[3],row[4],place,'UAE',phoneNumber]
        csvwriter = csv.writer(fp2)
        csvwriter.writerow(tableData)
        



    	
