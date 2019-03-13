import json
import io
import pymysql

#TO_DO: Migrate databases to PostGreSQL 

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Hazy9996',
                             db='254weather',
                             cursorclass=pymysql.cursors.DictCursor)
with open("city.list.min.json", "r", encoding = "UTF-8") as read_file:
    data = json.load(read_file)
    i = 55414
    print (len(data)) 
    while i < len(data):
        id1 = data[i]["id"]
        name = data[i]["name"]
        country = data[i]["country"]
        
        with connection.cursor() as cursor:
            sql = "INSERT INTO cities (id, name, country) VALUES (%s, %s, %s)"
            cursor.execute(sql, (id1, name, country))

        connection.commit()
        i += 1
    
""" with open("city_list.json", "r") as sum_file:
    data2 = json.load(sum_file)
    print(len(data2)) """