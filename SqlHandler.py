from flask import Flask,flash, redirect, url_for, session, logging, request
from passlib.hash import sha256_crypt
from FormHandler import RegisterForm

import pymysql

#TODO: Migrate Databases to PostGreSQL
#TODO: Add Home Town to user registration

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Hazy9996',
                             db='254weather',
                             cursorclass=pymysql.cursors.DictCursor)


def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor

        cur = connection.cursor()

        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        #Commit to DB
        connection.commit()

        # Close connection

        cur.close()

        flash ('You are now registered as a user and can log in', 'success')
    return True

def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']

        #Create cursor
        cur = connection.cursor()

        # Get user by username 
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            #Get stored hash
            data = cur.fetchone()
            password = data['password']

            #Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')

                return True