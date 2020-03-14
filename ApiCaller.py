from flask import Flask,flash, redirect, url_for, session, logging, request
from FormHandler import CitySearch
from pyowm import OWM


API_key = #The API key from OWM goes here
owm = OWM(API_key)

def search():
    form = CitySearch(request.form)
    search_id = int (form.search_term.data[:7])
    obs = owm.weather_at_id(search_id)
    weather = obs.get_weather()
    location = obs.get_location()
    data = [weather, location]
    return data

