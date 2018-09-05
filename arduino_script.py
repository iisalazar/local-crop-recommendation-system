import serial
import sqlite3
import time
import sys
from datetime import datetime

ser = serial.Serial('/dev/ttyACM0', 9600)
ser.baudrate=9600

#class Arduino:
#	def __init__(self, database):
#		self.database = database
#		self.ser = serial.Serial('/dev/ttyACM0', 9600)
#		self.ser.baudrate = 9600
# This function only writes on the database on every item
# In the future, change this to write on the database in a single 'commit' not commit-ing every script
#	def write_data(self, data):
#		connection = sqlite3.connect(self.database)
#		cursor = connection.cursor()
#		cursor.executescript("INSERT INTO soil(date_measured, soil_moisture) VALUES('{}', {});".format(datetime.now(), data))
#		connection.commit()
#
#	def read_data(self):
#		try:
#			read_ser = self.ser.readline()
#			print(str(read_ser))
#			return read_ser
#			time.sleep(1)
#		except KeyboardInterrupt:
#			print('\n Bye!')
#			sys.exit()
#		except:
#			print("Something fucked up!")
#for d in range(5):
#	write_data(d)

#if __name__ == '__main__':
#	app = Arduino('database.db')
#	a = app.read_data()
while True:
	read = ser.readline()
	print(read)
	time.sleep(1)
#		ard_data = app.read_data()
#		app.write_data(ard_data)
#		print(ard_data)
