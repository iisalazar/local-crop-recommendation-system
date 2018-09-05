import serial
import time
import sys
import sqlite3
from datetime import datetime

ser = serial.Serial('/dev/ttyACM0', 9600)
ser.baudrate = 9600

def read_data():
	try:
		read_ser = ser.readline()
		print(str(read_ser))
		return read_ser
	except:
		print("Something went wrong")

def write_data(data):
	connection = sqlite3.connect('database.db')
	cursor = connection.cursor()
	cursor.executescript("INSERT INTO soil(date_measured, soil_moisture) VALUES('{}', {});".format(datetime.now(), data))
	connection.commit()

while True:
	a = read_data()
	write_data(a)
#	print(a)
