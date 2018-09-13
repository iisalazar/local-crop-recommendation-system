import csv
import sys
import pprint
import statistics

# Gets the filename from the sys args
file = sys.argv[1]

# This function extracts data from the csv file
# Returns a dictionart file contating 'experimental' as the key
def extract_data(ranges):
	trials = {}
	f = open(file, 'rb')
	content = csv.reader(f)
	trial_key = 1
	c = []
	for row in content:
		c.append(row)
	for key, ranged in enumerate(ranges):
		r = ranged.split('-')
		# data[2]
		temperature = []
		# data[3]
		pressure = []
		# data[4]
		humidity = []
		for i in range(int(r[0])-1, int(r[1])):
			#print(c[i])
			temperature.append(float(c[i][2]))
			pressure.append(float(c[i][3]))
			humidity.append(float(c[i][4]))
		trials['trial {}'.format(trial_key)] = {'temperature': statistics.mean(temperature), 'pressure': statistics.mean(pressure), 'humidity': statistics.mean(humidity)}

		trial_key += 1
		print("----------------------- NEW TRIAL -----------------------")
	pprint.pprint(trials)
def main():
	ranges = raw_input("Write the ranges of your query (seperated by a comma ',')")
#	print(ranges)
	ranges = ranges.split(',')
	extracted_data = extract_data(ranges)
	#pprint.pprint(extracted_data)

if __name__ == '__main__':
	main()
