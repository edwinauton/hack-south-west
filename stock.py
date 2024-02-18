import json

import pandas as pd


class Stock:
	def __init__(self, json_file, stocks_owned):
		self.json_file = json_file
		self.number_owned = stocks_owned
		self.ticker = self.process_json()[0]
		self.start_price = self.process_json()[1]
		self.change = self.process_json()[2]
		self.equity = self.process_json()[3]
		self.daily_return = self.process_json()[4]

	def process_json(self):
		"""Parse the given json file and return the required values as a tuple"""
		with open(self.json_file) as f:
			file = json.load(f)
			ticker = file['Meta Data']['2. Symbol']
			all_values = list(file['Time Series (5min)'].values())
			start_price = float(all_values[-1]['1. open'])
			end_price = float(all_values[0]['4. close'])
			change = end_price - start_price
			equity = self.number_owned * end_price
			daily_return = self.number_owned * change
		return ticker, round(start_price, 2), round(change, 2), round(equity, 2), round(daily_return, 2)

	def create_graph(self):
		"""Return x and y values for the given file"""
		high_values = []
		time_values = []

		# Load the JSON data from the file
		with open(self.json_file) as f:
			file = json.load(f)

		# Extract high values and their corresponding time values
		for time_value, values in file['Time Series (5min)'].items():
			high_values.append(float(values['2. high']))
			time_values.append(pd.to_datetime(time_value))

		# Create DataFrame
		df = pd.DataFrame({'Time': time_values, 'High': high_values})

		# Return the x and y values
		return df['Time'], df['High']
