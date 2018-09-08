import csv
import sys
import sqlite3
import pprint

def extract_data(db_name, table_name):
	try:
		connection = sqlite3.connect(db_name)
		cursor = connection.cursor()
		cursor.execute('SELECT * FROM {};'.format(table_name))
		data = cursor.fetchall()
		print("Successfully grabbed data")
	except sqlite3.Error:
		if connection:
			print("Error in retrieveing data!")
	finally:
		if connection:
			connection.close()
		if data:
			return data

def write_data_to_csv(content):
	with open('environment.csv', 'wb') as env:
		writer = csv.writer(env)
		writer.writerows(content)

if __name__ == '__main__':
	d = extract_data(sys.argv[1], sys.argv[2])
	pprint.pprint(d)
	write_data_to_csv(d)
