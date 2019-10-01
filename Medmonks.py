import sys
import requests
import csv
from bs4 import BeautifulSoup
import phonenumbers
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from geotext import GeoText
links=[]
docterName=[]
url="https://medmonks.com/best-doctors/india"
result=requests.get(url)
src = result.content
soup = BeautifulSoup(src, "lxml")
dataForScrap=soup.find_all("a",{"class":"color-blue"})
for link in dataForScrap:
	print(link.attrs['href'])
	links.append(link.attrs['href'])
