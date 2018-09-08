import requests
import sys
import pprint

api_key = '5ed50787e4f36a97057b04bdf51623f1'
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'
r = requests.get(url.format(sys.argv[1], api_key)).json()
pprint.pprint(r)
