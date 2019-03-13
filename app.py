from pyowm import OWM
import json
from FormHandler import RegisterForm, SearchForm, CitySearch
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from functools import wraps
import SqlHandler
import weather
import ApiCaller


app = Flask(__name__)



@app.route('/')
def index():
    return render_template("home.html")

def user_searched(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		if 'user_searched' in session:
			return f(*args, **kwargs)
		else:
			flash('Unauthorized, Please login and search', 'danger')
			return redirect(url_for('dashboard'))
		return wrapper

# Check if user is logged in 
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Unauthorized, Please login', 'danger')
			return redirect(url_for('login'))
	return wrap

@app.route('/dashboard', methods=['GET', 'POST'])
@is_logged_in
def dashboard():
	form = SearchForm(request.form)
	if request.method == 'POST' and form.validate():
		session['user_searched'] = True
		session['form_data'] = form.city.data
		if weather.get_city_id():
			return render_template('myweather.html')
	session['user_searched'] = False	
	return render_template("dashboard.html")

""" @user_searched
def myweather():
	return render_template('myweather.html') """

#Register new user with assistance from FormHandler class and SqlHandler
@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		if SqlHandler.register():
			return redirect(url_for('login'))
	return render_template('register.html', form = form)
		

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		if SqlHandler.login():
				return redirect(url_for('dashboard'))
		else:
			error = 'Invalid login'
			return render_template('login.html', error = error)	
		
	""" else:
		error = 'Username not found'
		return render_template('login.html', error = error) """ 	

	return render_template('login.html')	

@app.route('/logout')
def logout():
	session.clear()
	flash('You are now logged out', 'success')
	return redirect(url_for('login'))

# Search for particular weather instance
@app.route('/weather_search', methods = ['GET', 'POST'])
def weather_search():
	if request.method == 'POST':
		weather = ApiCaller.search()
		status = weather.get_status()
		detailed_status = weather.get_detailed_status()
		clouds = weather.get_clouds()
		rain = weather.get_rain()
		snow = weather.get_snow()
		wind = weather.get_wind()
		humidity = weather.get_humidity()
		pressure = weather.get_pressure()
		temperature = weather.get_temperature(unit = 'celsius')
		weather_data = (status, detailed_status, clouds, rain, snow, wind, humidity, pressure, temperature)
		return render_template('cityweather.html',data = weather_data)


		






if __name__ == '__main__':
	app.secret_key = 'secret123'
	app.run(debug=True) 