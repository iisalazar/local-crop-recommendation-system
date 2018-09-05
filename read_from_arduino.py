import serial
import time
import sys

ser = serial.Serial('/dev/ttyACM0', 9600)
ser.baudrate=9600
while True:
	try:
		read_ser = ser.readline()
		print(str(read_ser))
		time.sleep(1)
	except KeyboardInterrupt:
		print("\n Babye!!!")
		sys.exit()
	except:
		print("Something fucked up!")

