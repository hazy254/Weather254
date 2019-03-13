from pyowm import OWM
from flask import session

import pymysql

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Hazy9996',
                             db='254weather',
                             cursorclass=pymysql.cursors.DictCursor)

API_key = '7a20bb50e3dd278369161f06ba152895'
owm = OWM(API_key)

def get_city_id():
    data = session.get('form_data', None)
    user_search = data.upper()
    cities = []
    with connection.cursor() as cursor:
        sql = "SELECT * FROM cities WHERE UPPER(name) LIKE %s "
        result = cursor.execute(sql, (user_search))
        if result > 0:
            for row in cursor:
                cities.append(row)
        session['cities'] = cities


    connection.commit()
    return True    
