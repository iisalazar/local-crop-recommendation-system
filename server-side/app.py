#main.py

from gevent import monkey
monkey.patch_all()


from datetime import datetime
import time
from threading import Thread
from flask import Flask, render_template, session, request, jsonify
from flask.ext.socketio import SocketIO, emit, join_room, disconnect
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None


def background_stuff():
    """ Let's do it a bit cleaner """
    while True:
        time.sleep(1)
        t = str(time.clock())
        socketio.emit('message', {'data': 'This is data', 'time': t}, namespace='/test')


def another_background_stuff():
    while True:
        time.sleep(1)
        data = 'This is some data'
        socketio.emit('sent', {'data': data}, namespace='/test')
@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_stuff)
        thread.start()
    threading = Thread(target=another_background_stuff)
    threading.start()
    return render_template('receive.html')

@socketio.on('my event', namespace='/test')
def my_event(msg):
    print msg['data']



@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')
	


ROOT_DIR = os.path.dirname(os.path.abspath('.'))

# Database stuff
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

def get_env():
    while True:
        time.sleep(1)
        socketio.emit('receive_weather', {'temperature': temperature, 'humidity': humidity, 'pressure': pressure}, namespace='receive_weather')

@app.route('/receive_weather')
def receive_weather():
    threading = None
    threading = Thread(target=get_env)
    threading.run()
    return render_template('get_env.html')

@app.route('/query')
def query():
    env = Environment.query.all()
    soil = Soil.query.all()
    env_query = []
    soil_query = {}
    for r in range(len(env)):
        env_query.append(env[r].serialize)
        #env_query['Query '+str(r)] = env[r].serialize
    for s in range(len(soil)):
        soil_query['Query ' + str(s)] = soil[s].serialize

    return render_template('query.html', Environment_data=env_query, Soil_data=soil_query)

	
if __name__ == '__main__':
    socketio.run(app)
