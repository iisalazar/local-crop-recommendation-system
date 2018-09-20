from gevent import monkey
monkey.patch_all()


import time
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from logic import Calculate
import random
from flask.ext.socketio import SocketIO, emit, join_room, disconnect
from threading import Thread
import logging
logging.basicConfig()
thread = None
# getting the root directory of project
ROOT_DIR = os.path.dirname(os.path.abspath('.'))
# Instantiate the app
app = Flask(__name__)
socketio = SocketIO(app)
# Setup config for connecting to the sqlite database at ROOT_DIR
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+ ROOT_DIR + '/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
# For model purposes 
class Environment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_measured = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	temperature = db.Column(db.Float, nullable=False)
	air_pressure = db.Column(db.Float, nullable=False)
	humidity = db.Column(db.Float, nullable=False)

	# For serialization queries
	# This method returns a dictionary that can be helpful for JSON request
	@property
	def serialize(self):
		return {
			'id': self.id,
			'date_measured': self.date_measured,
			'temperature': self.temperature,
			'air_pressure': self.air_pressure,
			'humidity': self.humidity
		}

# For model purposes 
class Soil(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_measured = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	soil_moisture = db.Column(db.Float, nullable=False)

	# For serialization queries
	# This method returns a dictionary that can be helpful for JSON request
	@property
	def serialize(self):
		return {
			'id': self.id,
			'date_measured': self.date_measured,
			'soil_moisture': self.soil_moisture
		}
	
# This is the home ('/') directory
# This method returns a JSON object containing soil and environment data from the database
@app.route('/api/')
def api():
	env = Environment.query.all()
	soil = Soil.query.all()
	env_query = {}
	soil_query = {}
	for r in range(len(env)):
		env_query['Query '+str(r)] = env[r].serialize
	for s in range(len(soil)):
		soil_query['Query ' + str(s)] = soil[s].serialize

	return jsonify({"Environment_data": env_query, "Soil_data": soil_query})

# This is a template for processing custom requests
@app.route('/')
def main():
	env = Environment.query.all()
	soil = Soil.query.all()
	env_query = {}
	soil_query = {}
	for r in range(len(env)):
		env_query['Query ' + str(r)] = env[r].serialize
	for s in range(len(soil)):
		soil_query['Query ' + str(s)] = soil[s].serialize

	return render_template("main.html", environment=env_query, soil=soil_query)
	#return jsonify({"Environmental data": env_query, "Soil data": soil_query})

# This method is used for creating a content inside the database
# Use this only for development only

# This route is used for querying logic requests
# That is, when a user want's to query a recommended crop for it
@app.route('/logic/')
def log():
	calculate = Calculate()
	env = Environment.query.all()
	soil = Soil.query.all()
	temperature = []
	air_pressure = []
	humidity = []
	soil_moisture = []

	for i in env:
		temperature.append(i.serialize['temperature'])
		air_pressure.append(i.serialize['air_pressure'])
		humidity.append(i.serialize['humidity'])

	for s in soil:
		soil_moisture.append(s.serialize['soil_moisture'])

	temp = calculate.get_mean(data=temperature)
	pres = calculate.get_mean(data=air_pressure)
	humd = calculate.get_mean(data=humidity)
	soil_h = calculate.get_mean(data=soil_moisture)
	print(temp)
	print(pres)
	print(humd)
	print(soil_h)
	return render_template('logic.html', temperature=temp, pressure=pres, soil_moisture=soil_h)
	#return jsonify({"Temperature": temp, "Pressure": pres, "Humidity": humd, "Soil Moisture": soil_h})


@socketio.on('start isabela')
def send():
    socketio.emit('isabela', "data");
@socketio.on('custom event')
def print_message(msg):
    print(msg)

@socketio.on('receive message')
def send_message():
    data = 'C'
    emit('receive message', data=data)
@app.route('/text')
def text():
    return render_template('text.html')

def something():
	signature = Environment(date_measured=datetime.now(), temperature=random.randrange(1000, 1200), air_pressure=random.randrange(11000, 12500), humidity=random.randrange(10,20))
	db.session.add(signature)
	db.session.commit()

	soil = Soil(date_measured=datetime.now(), soil_moisture=random.randrange(0,20))
	db.session.add(soil)
	db.session.commit()
	return

def handle_data():
	while True:
		time.sleep(1)
		socketio.emit('receive', {"data": "Something"}, namespace='/test')

@app.route('/receive')
def receive():
	global thread
	if thread is None:
		thread = Thread(target=handle_data)
		thread.start()

	return render_template("receive.html")

if __name__ == '__main__':
	socketio.run(app)