import random
import sys

import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QLabel, QDialog, QGridLayout, QScrollArea, QWidget, QHBoxLayout, QVBoxLayout, QPushButton)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


def create_button(text):
	button = QPushButton()
	button.setText(text)
	return button


def create_label(text):
	label = QLabel(text)
	label.setAlignment(Qt.AlignCenter)
	return label


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

		self.table.addLayout(header)

		# Add spacing after heading
		self.table.insertSpacing(1, 25)

		for i in range(1, 20):
			# Create row
			row = QHBoxLayout()

			# Ticker Button
			ticker = create_button("[Ticker]")
			row.addWidget(ticker)

			# Last Price
			last_price = create_label("[Last Price]")
			row.addWidget(last_price)

			# Change
			change = create_label("[Change]")
			row.addWidget(change)

			# Equity
			equity = create_label("[Equity]")
			row.addWidget(equity)

			# Daily Return
			daily_return = create_label("[Return]")
			row.addWidget(daily_return)

			# Buy Button
			buy_button = create_button("Buy")
			row.addWidget(buy_button)

			# Sell Button
			sell_button = create_button("Sell")
			row.addWidget(sell_button)

			# Add row to vbox (table)
			self.table.addLayout(row)

		# Setup Grid
		layout = QGridLayout()

		# Titles
		profile_value = create_label("Profile Value: [N/A]")
		layout.addWidget(profile_value, 0, 1, 1, 1)

		daily_gain = create_label("Today's Gain: [N/A]")
		layout.addWidget(daily_gain, 1, 1, 1, 1)

		# Scrollable Table
		self.widget.setLayout(self.table)
		self.scroll.setWidgetResizable(True)
		self.scroll.setWidget(self.widget)
		layout.addWidget(self.scroll, 0, 3, 3, 1)

		# Graph
		layout.addWidget(self.canvas, 2, 0, 1, 3)
		self.plot([random.random() for _ in range(50)])

		# Window Properties
		self.setWindowTitle('Stock Trading Simulator')
		self.setGeometry(10, 10, 1700, 700)
		self.setLayout(layout)
		self.show()

	def plot(self, data):
		"""Plots the data given in an array on the graph shown in the window"""
		self.figure.clear()
		graph = self.figure.add_subplot(111)
		graph.plot(data, '*-')
		self.canvas.draw()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Window()
	sys.exit(app.exec_())
