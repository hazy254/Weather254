from flask import Flask,flash, redirect, url_for, session, logging, request
from passlib.hash import sha256_crypt
from FormHandler import RegisterForm

from psycopg2 import pool

#TODO: Migrate Databases to PostGreSQL
#TODO: Add Home Town to user registration


class Database:

    __connection_pool = None

    @staticmethod
    def initialise(**kwargs):
        Database.__connection_pool = pool.SimpleConnectionPool(1, 10, **kwargs)

    @staticmethod
    def get_connection():
        return Database.__connection_pool.getconn()

    @staticmethod
    def return_connection(connection):
        Database.__connection_pool.putconn(connection)

    @staticmethod
    def close_all_connections():
        Database.__connection_pool.closeall()


class CursorFromConnectionPool:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = Database.get_connection()
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if exception_value:  # This is equivalent to `if exception_value is not None`
            self.conn.rollback()
        else:
            self.cursor.close()
            self.conn.commit()
        Database.return_connection(self.conn)

#Initialise database with Database.initalise(user credentials go here)

def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        city = form.city.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor

        with CursorFromConnectionPool() as cursor:

            cursor.execute("INSERT INTO users(name, email, username, password, city) VALUES(%s, %s, %s, %s, %s)", (name, email, username, password, city))

            

            flash ('You are now registered as a user and can log in', 'success')
    return True

def login():
    if request.method == 'POST':
        username = str(request.form['username'])
        password_candidate = request.form['password']

        with CursorFromConnectionPool() as cursor:
            
            # Get user by username 
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            data = cursor.fetchone()


            if data:
                #Get stored hash
                password = data[2]
                #Compare Passwords
                if sha256_crypt.verify(password_candidate, password):
                    session['logged_in'] = True
                    session['username'] = username

                    flash('You are now logged in', 'success')

                    return True

