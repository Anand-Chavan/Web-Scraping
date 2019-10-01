import re
import csv
fp=open("Iaaps-India.csv","r")
fp2=open("pincode.txt","w")
line=fp.readlines()
k=1
for data in line:
	if(len(data)>10):
		reg = re.compile('^.*(?P<zipcode>\d{6}).*$')
		match = reg.match(data)
		if(match):
			pincode=match.groupdict()['zipcode']
			csvwriter = csv.writer(fp2)
			csvwriter.writerow(pincode)
			print(pincode)
			k=k+1
		else:
			pincode=""
			print(pincode)
			k=k+1

		

print(k)

	
	
	