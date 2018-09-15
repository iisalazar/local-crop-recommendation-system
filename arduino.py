import serial
import csv
import sys
import time
import re
import statistics

ser = serial.Serial('/dev/ttyACM0', 9600)
ser.baudrate = 9600

digit_regex = re.compile(r'\d\d')

def read_serial(range_value):
	serial_value = []
	for i in range(range_value):
		try:
			read_serial = digit_regex.search(ser.readline())
			print(read_serial.group())
			serial_value.append(int(read_serial.group()))
			time.sleep(1)
		except KeyboardInterrupt:
			sys.exit()
		except:
			print("Something went wrong!")
	return serial_value

def write_data(data):
	with open('soil.csv', 'wb') as file:
		writer = csv.writer(file)
		for d in data:
			writer.writerow([d])

if __name__ == '__main__':
	serial = read_serial(int(sys.argv[1]))
	print(statistics.mean(serial))
	#write_data(serial)