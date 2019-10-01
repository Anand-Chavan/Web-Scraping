import requests
import csv
from bs4 import BeautifulSoup
# from geotext import GeoText
# sentence = "I am from Delhi"
# places = GeoText(sentence)
# from geograpy import extraction

# e = extraction.Extractor(url='https://www.isaps.org/listing/dr-ahmed-afifi-md/')
# e.find_entities()

# # # You can now access all of the places found by the Extractor
# print(e.places)

# import geograpy

# text='I live in Kadawatha'

# places = geograpy.get_place_context(text=text)

# print(places.country_cities)

# import geonamescache

# gc = geonamescache.GeonamesCache()
# countries = gc.get_cities_by_name("india")
# # print countries dictionary
# for city in countries:
# 	print(city)
# you really wanna do something more useful with the data...

# import geograpy3
# # link = 'http://www.bbc.com/news/world-europe-26919928'
# # places = geograpy3.get_place_context(url = link)

# # text_input = "Perfect just Perfect! It's a perfect storm for Nairobi"
# more_places = geograpy3.get_place_context(text = "Perfect just Perfect! It's a perfect storm for Nairobi")

# print(more_places.cities)	
indiaCityList=[]
ukCityList=[]
usaCityList=[]
arabCityList=[]
url="http://www.krisia.com/city_list.htm"
result=requests.get(url)
src = result.content
soup = BeautifulSoup(src, "lxml")
listOfCities=soup.find_all("td",{"class":"resultsPane"})
for city in listOfCities:
	indiaCityList.append(city.text)
