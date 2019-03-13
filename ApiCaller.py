from flask import Flask,flash, redirect, url_for, session, logging, request
from FormHandler import CitySearch
from pyowm import OWM
import json 
import requests


API_key = '7a20bb50e3dd278369161f06ba152895'
owm = OWM(API_key)

def search():
    form = CitySearch(request.form)
    search_id = int (form.search_term.data[:7])
    obs = owm.weather_at_id(search_id)
    weather = obs.get_weather()
    return weather

