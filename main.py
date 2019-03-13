from pyowm import OWM
import json 
import requests
#This program aims to make use of the OpenWeatherMap API to display daily and weekly weather
#This is done using the pyowm wrapper library for the API to make calls and retrieve data.

#First is to connect to the API using the key provided
API_key = '7a20bb50e3dd278369161f06ba152895'
owm = OWM(API_key)

#To get The data for a particular location
#TO_DO: Get the list of location IDs from JSon file and parse here. Try using a dropdown menu if possible.
""" with open("city.list.min.json", "r", encoding = 'UTF-8') as read_file:
    data = json.load(read_file)
    i = 0
    while i < 10:
        print (data[i]["name"], end = " - ")
        print (data[i]["id"], end = ' - ')
        id = data[i]["id"]
        obs = owm.weather_at_id(id)
        weather = obs.get_weather()
        print (weather.get_rain())
        i += 1
        
 """
obs = owm.weather_at_id(703363)
w = obs.get_weather()
print (repr(w))
#TO_DO: 