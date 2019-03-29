from pyowm import OWM
from flask import session



API_key = '7a20bb50e3dd278369161f06ba152895'
owm = OWM(API_key)
reg = owm.city_id_registry()

def get_city_id():
    data = session.get('form_data', None)
    user_search = data.title()
    cities = []
    result = reg.ids_for(user_search)
    if result:
        for city in result:
            cities.append(city)
        session['cities'] = cities
    return True    
