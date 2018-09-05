import Adafruit_DHT, Adafruit_BMP.BMP085 as Sensor2
import time
import sys
import statistics
import sqlite3
from datetime import datetime
class WeatherStation:
		def __init__(self):
			self.sensor1 = Adafruit_DHT.DHT22
			self.sensor2 = Sensor2.BMP085()
			self.sensor1_pin = 22
		def get_data(self):
			self.humidity, self.temperature = Adafruit_DHT.read_retry(self.sensor1, self.sensor1_pin)
			self.pressure = self.sensor2.read_pressure()
			self.temp = self.sensor2.read_temperature()
			self.altitude = self.sensor2.read_altitude()
			return {
					"Humidity": self.humidity, 
					#"Temperature": statistics.mean([self.temperature, self.temp]),
					"Temperature 1" : self.temperature,
					"Temperature 2" : self.temp,
					"Pressure" : self.pressure,
					"Altitude" : self.altitude
				}
		def write_data(self):
			try:
				connection = sqlite3.connect('database.db')
				print("Debug 1")
				cursor = connection.cursor()
				print("Debug 2")
				cursor.executescript("INSERT INTO environment(date_measured, temperature, air_pressure, humidity) VALUES('{}', {}, {}, {});".format(datetime.now(), statistics.mean([self.temperature, self.temp]), self.pressure, self.humidity))
				print("Debug 3")
				cursor.commit()
				print("Debug 4")
			except sqlite3.Error:
				print("Something went wrong! Rolling back!")
				if connection:
					connection.rollback()
			except:
				print("Putang ina")
			finally:
				if connection:
					connection.close()

if __name__ == '__main__':
	while True:
		weather_station = WeatherStation()
		data = weather_station.get_data()
		print(data)
		weather_station.write_data()
		time.sleep(1)
