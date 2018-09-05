import Adafruit_BMP.BMP085 as BMP085

sensor = BMP085.BMP085()

print("Temperature: {} *C".format(sensor.read_temperature()))
