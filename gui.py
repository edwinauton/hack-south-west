import os
import sys
from share import Share

import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QLabel, QDialog, QGridLayout, QScrollArea, QWidget, QHBoxLayout, QVBoxLayout, QPushButton)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


def create_button(text):
	"""Creates a button with the given text"""
	button = QPushButton()
	button.setText(text)
	return button


def create_label(text):
	"""Creates a label with the given text and centres it"""
	label = QLabel(text)
	label.setAlignment(Qt.AlignCenter)
	return label


def get_shares_list():
	shares_list = list()

	for subdir, dirs, files in os.walk("resources"):
		for file in files:
			filepath = subdir + os.sep + file
			if filepath.endswith(".json"):
				shares_list.append(Share(filepath, 10))

	return shares_list


class Window(QDialog):
	def __init__(self, parent=None):
		super(Window, self).__init__(parent)
		self.figure = plt.figure()
		self.canvas = FigureCanvas(self.figure)
		self.scroll = QScrollArea()
		self.widget = QWidget()
		self.table = QVBoxLayout()
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

		equity = create_label("Your Equity")
		header.addWidget(equity)

		daily_return = create_label("Today's Return")
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
			# Create row
			row = QHBoxLayout()

			# Ticker Button
			ticker = create_button(str(share.ticker))
			row.addWidget(ticker)

			# Last Price
			last_price = create_label(str(share.start_price))
			row.addWidget(last_price)

			# Change
			change = create_label(str(share.change))
			row.addWidget(change)

			# Equity
			equity = create_label(str(share.equity))
			row.addWidget(equity)

			# Daily Return
			daily_return = create_label(str(share.daily_return))
			row.addWidget(daily_return)

			# Buy Button
			buy_button = create_button("Buy")
			row.addWidget(buy_button)

			# Sell Button
			sell_button = create_button("Sell")
			row.addWidget(sell_button)

			# Share Number
			shares_owned = create_label(str(share.number_owned))
			row.addWidget(shares_owned)

			# Add row to table
			self.table.addLayout(row)

		# Setup Grid
		layout = QGridLayout()

		# Titles
		profile_value = create_label(f"Profile Value: {round(sum(share.equity for share in shares), 2)}")
		layout.addWidget(profile_value, 0, 1, 1, 1)

		daily_gain = create_label(f"Today's Return: {round(sum(share.daily_return for share in shares), 2)}")
		layout.addWidget(daily_gain, 1, 1, 1, 1)

		# Scrollable Table
		self.widget.setLayout(self.table)
		self.scroll.setWidgetResizable(True)
		self.scroll.setWidget(self.widget)
		layout.addWidget(self.scroll, 0, 3, 3, 1)

		# Graph
		layout.addWidget(self.canvas, 2, 0, 1, 3)
		self.plot(shares[0])

		# Window Properties
		self.setWindowTitle('Stock Trading Simulator')
		self.setGeometry(10, 10, 1700, 700)
		self.setLayout(layout)
		self.show()

	def plot(self, share):
		"""Plots the data given in an array on the graph shown in the window"""
		self.figure.clear()
		graph = self.figure.add_subplot(111)
		data = share.create_graph()
		graph.plot(data[0], data[1],  marker='.', linestyle='-')
		self.canvas.draw()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Window()
	sys.exit(app.exec_())
