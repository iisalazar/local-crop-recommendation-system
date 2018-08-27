from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
# getting the root directory of project
ROOT_DIR = os.path.dirname(os.path.abspath('.'))
# Instantiate the app
app = Flask(__name__)
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
@app.route('/', methods=['GET'])
def home():
	env = Environment.query.all()
	soil = Soil.query.all()
	return render_template('main.html', env_data=env, soil_data=soil)

# This method is used for creating a content inside the database
# Use this only for development only
def something():
	signature = Environment(date_measured=datetime.now(), temperature=1234.1, air_pressure=12351.4, humidity=10.13)
	db.session.add(signature)
	db.session.commit()

	soil = Soil(date_measured=datetime.now(), soil_moisture=3.14156)
	db.session.add(soil)
	db.session.commit()

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')