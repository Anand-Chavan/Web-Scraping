# import requests
# import csv
# from bs4 import BeautifulSoup
# url="http://apsi.in/"
# result=requests.get(url)
# src = result.content
# soup = BeautifulSoup(src, "lxml")
# driver.execute_script("return document.title")
# print(soup)
from selenium import webdriver

driver = webdriver.Chrome('C:/Users/WorkStation/Desktop/chromedriver.exe')

driver.execute_script("return document.title")