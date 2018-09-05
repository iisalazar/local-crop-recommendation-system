import serial
import sqlite3
import time
import sys
from datetime import datetime

def write_data():
	connection = sqlite3.connect("database.db")
	cursor = connection.cursor()
