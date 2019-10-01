import csv 
import re
import datetime
from geotext import GeoText
import phonenumbers
fp=open("The American Society for Aesthetic Plastic Surgery-India.csv","r")
# line=fp.readlines()
# for data in line:
p = re.compile(r'^(\s+)?(Mr(\.)?|Mrs(\.)?)?(?P<FIRST_NAME>.+)(\s+)(?P<LAST_NAME>.+)$', re.IGNORECASE)

fp2=open("The American Society for Aesthetic Plastic-Surgery-India.csv","w")	
column=['first_name','last_name','degree','phoneNumber','address','pincode','city','Country','memberType','website']
csvwriter = csv.writer(fp2)
csvwriter.writerow(column)
# print(len(column))

with fp as csv_file:
    csv_reader = csv.reader(csv_file)
    print(csv_reader)
    for row in csv_reader:
        address=row[4]
        places = GeoText(address)
        city=places.cities
        place=""
        if(city!=[]):
            place=city[0]

    
        tableData=[row[0],row[1],row[2],row[3],row[4],row[5],place,'IN',row[6],row[7]]
        csvwriter = csv.writer(fp2)
        csvwriter.writerow(tableData)
        



    	
