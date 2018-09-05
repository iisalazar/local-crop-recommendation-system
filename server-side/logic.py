import statistics as stat

class Calculate:
	def get_mean(self, *args, **kwargs):
		try:
			data = stat.mean(kwargs['data'])
			return data
		except stat.StatisticsError:
			print("Can't calculate the mean. Something went wrong")
		return

	def get_mode(self, *args, **kwargs):
		try:
			data = stat.mode(kwargs['data'])
			return data
		except stat.StatisticsError:
			print("Can't calculate the mode. Better check the data")
		return
	
	def get_median(self, *args, **kwargs):
		try:
			data = stat.median(kwargs['data'])
		except stat.StatisticsError:
			print("Can't calculate the median. Something went wrong")
		return
	
	def get_data(self, *args, **kwargs):
		return kwargs['data']