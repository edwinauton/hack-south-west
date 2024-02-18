import os
import json
import sys
from functools import partial

import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QLabel, QGridLayout, QScrollArea, QWidget, QHBoxLayout, QVBoxLayout,
							 QPushButton, QSizePolicy)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from share import Share


def create_button(text):
	"""Creates a button with the given text"""
	button = QPushButton()
	button.setText(text)
	return button


def create_label(text):
	"""Creates a label with the given text and centres it"""
	label = QLabel(text)
	label.setAlignment(Qt.AlignCenter)
	label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
	return label


def get_shares_list():
	# Read shares stored in file
	with open("share_record.json") as f:
		data = json.load(f)

	shares_list = []

	# Read data from files provided by API
	for subdir, dirs, files in os.walk("resources"):
		for file in files:
			filepath = subdir + os.sep + file
			if file.endswith(".json"):
				filename = os.path.splitext(file)[0]
				shares_list.append(Share(filepath, data[filename]))

	return shares_list


class Window(QWidget):
	def __init__(self, parent=None):
		super(Window, self).__init__(parent)
		self.figure = plt.figure()
		self.canvas = FigureCanvas(self.figure)
		self.scroll = QScrollArea()
		self.widget = QWidget()
		self.table = QVBoxLayout()
		self.profile_value = QLabel()
		self.overall_return = QLabel()
		self.ticker = QPushButton()
		self.last_price = QLabel()
		self.change = QLabel()
		self.equity = QLabel()
		self.daily_return = QLabel()
		self.buy_button = QPushButton()
		self.sell_button = QPushButton()
		self.shares_owned = QLabel()
		self.init()

	def init(self):
		# Table Header
		header = QHBoxLayout()

		ticker = create_label("Ticker")
		header.addWidget(ticker)

		last_price = create_label("Last Price")
		header.addWidget(last_price)

		change = create_label("Change")
		header.addWidget(change)

		equity = create_label("Equity")
		header.addWidget(equity)

		daily_return = create_label("Return")
		header.addWidget(daily_return)

		spacer = create_label("")
		header.addWidget(spacer)
		header.addWidget(spacer)

		shares_owned = create_label("Shares Owned")
		header.addWidget(shares_owned)

		self.table.addLayout(header)

		# Add spacing after heading
		self.table.insertSpacing(1, 25)

		shares = get_shares_list()

		for share in shares:
			# Setup Row
			row = QHBoxLayout()

			# Ticker Button
			self.ticker = create_button(str(share.ticker))
			self.ticker.clicked.connect(partial(self.update_graph, share))
			row.addWidget(self.ticker)

			# Last Price
			self.last_price = create_label(str(share.start_price))
			row.addWidget(self.last_price)

			# Change
			self.change = create_label(str(share.change))
			row.addWidget(self.change)

			# Equity
			self.equity = create_label(str(share.equity))
			row.addWidget(self.equity)

			# Daily Return
			self.daily_return = create_label(str(share.daily_return))
			row.addWidget(self.daily_return)

			self.shares_owned = create_label(str(share.number_owned))

			# Buy Button
			self.buy_button = create_button("Buy")
			self.buy_button.clicked.connect(partial(self.update_shares, 1, share))
			row.addWidget(self.buy_button)

			# Sell Button
			self.sell_button = create_button("Sell")
			self.sell_button.clicked.connect(partial(self.update_shares, -1, share))
			row.addWidget(self.sell_button)

			# Share Number
			row.addWidget(self.shares_owned)
			self.table.addLayout(row)

		# Setup Grid
		layout = QGridLayout()

		# Titles
		self.profile_value = create_label(f"Profile Value: {round(sum(share.equity for share in shares), 2)}")
		layout.addWidget(self.profile_value, 0, 1, 1, 1)
		self.overall_return = create_label(f"Today's Return: {round(sum(share.daily_return for share in shares), 2)}")
		layout.addWidget(self.overall_return, 1, 1, 1, 1)

		# Scrollable Table
		self.widget.setLayout(self.table)
		self.scroll.setWidgetResizable(True)
		self.scroll.setWidget(self.widget)
		layout.addWidget(self.scroll, 0, 3, 3, 1)

		# Graph
		layout.addWidget(self.canvas, 2, 0, 1, 3)
		self.plot((shares[0].create_graph()[0], sum(share.create_graph()[1] for share in shares)))

		# Window Properties
		self.setWindowTitle('Stock Trading Simulator')
		self.setGeometry(10, 10, 1700, 700)
		self.setLayout(layout)
		self.show()

	def update_graph(self, share):
		self.plot(share.create_graph())
		self.update()

	def update_shares(self, value, share):
		share.number_owned += value

		# Save shares information to file
		with open("share_record.json") as f:
			data = json.load(f)
			data[share.ticker] = share.number_owned

		self.update()

	def plot(self, data):
		"""Plots the data given in an array on the graph shown in the window"""
		self.figure.clear()
		graph = self.figure.add_subplot(111)
		graph.plot(data[0], data[1], marker='.', linestyle='-')
		self.canvas.draw()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Window()
	sys.exit(app.exec_())
