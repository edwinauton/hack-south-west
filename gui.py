import os
import json
import sys
from functools import partial

import matplotlib.pyplot as plt
from matplotlib import dates as mdates
import mplcursors
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QLabel, QGridLayout, QScrollArea, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QSizePolicy, QFrame)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtGui import QIcon
from share import Share


def create_button(text):
	button = QPushButton()
	button.setText(text)
	return button


def create_line():
	line = QFrame()
	line.setFrameShape(QFrame.HLine)
	line.setObjectName("line")
	return line


def format(data):
	string = str(data)
	if string[0] == "-":
		return "-$" + string[1:]
	else:
		return "$" + string


def colour(label):
	if "-" in label.text():
		label.setObjectName("loss")
	else:
		label.setObjectName("gain")


def colour_heading(heading):
	if "-" in heading.text():
		heading.setObjectName("heading_loss")
	else:
		heading.setObjectName("heading_gain")


def create_label(text):
	label = QLabel(text)
	label.setAlignment(Qt.AlignCenter)
	label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
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
		self.portfolio_value = QLabel()
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

		spacer = create_label("")
		header.addWidget(spacer)

		price = create_label("Price")
		price.setObjectName("subheading")
		header.addWidget(price)

		change = create_label("Change")
		change.setObjectName("subheading")
		header.addWidget(change)

		equity = create_label("Equity")
		equity.setObjectName("subheading")
		header.addWidget(equity)

		daily_return = create_label("Return")
		daily_return.setObjectName("subheading")
		header.addWidget(daily_return)

		header.addWidget(spacer)
		header.addWidget(spacer)

		shares_owned = create_label("Shares Owned")
		shares_owned.setObjectName("subheading")
		header.addWidget(shares_owned)

		self.table.addLayout(header)
		self.table.addWidget(create_line())

		# Add spacing after heading
		self.table.insertSpacing(1, 10)
		self.table.addWidget(create_line())

		shares = get_shares_list()

		for share in shares:
			# Setup Row
			row = QHBoxLayout()

			# Ticker Button
			self.ticker = create_button(str(share.ticker))
			self.ticker.clicked.connect(partial(self.update_graph, share))
			row.addWidget(self.ticker)

			# Last Price
			value = format(share.start_price)
			self.last_price = create_label(value)
			row.addWidget(self.last_price)

			# Change
			value = format(share.change)
			self.change = create_label(value)
			colour(self.change)
			row.addWidget(self.change)

			# Equity
			value = format(share.equity)
			self.equity = create_label(value)
			row.addWidget(self.equity)

			# Daily Return
			value = format(share.daily_return)
			self.daily_return = create_label(value)
			colour(self.daily_return)
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
			self.table.addWidget(create_line())

		# Setup Grid
		layout = QGridLayout()

		# Titles
		value = format(round(sum(share.equity for share in shares), 2))
		self.portfolio_value = create_label(f"Portfolio Value: {value}")
		self.portfolio_value.setObjectName("heading")
		layout.addWidget(self.portfolio_value, 0, 1, 1, 1)
		value = format(round(sum(share.daily_return for share in shares), 2))
		self.overall_return = create_label(f"Today's Return: {value}")
		colour_heading(self.overall_return)
		layout.addWidget(self.overall_return, 1, 1, 1, 1)

		# Scrollable Table
		self.widget.setLayout(self.table)
		self.scroll.setWidgetResizable(True)
		self.scroll.setWidget(self.widget)
		self.scroll.setFrameShape(QFrame.NoFrame)
		layout.addWidget(self.scroll, 0, 3, 3, 1)

		# Graph
		layout.addWidget(self.canvas, 2, 0, 1, 3)
		self.plot((shares[0].create_graph()[0], sum(share.create_graph()[1] for share in shares)))

		# Window Properties
		self.setWindowTitle('Stock Trading Simulator')
		self.setWindowIcon(QIcon("icon.jpg"))
		self.setGeometry(10, 10, 2560, 1440)
		self.setMinimumSize(1500, 900)
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
		self.figure.clear()
		graph = self.figure.add_subplot(111)
		graph.xaxis.set_visible(False)
		graph.yaxis.label.set_color('#2da9b9')
		graph.tick_params(axis='y', colors='#2da9b9')
		for axis in ['top', 'bottom', 'left', 'right']:
			graph.spines[axis].set_color('#2da9b9')
			graph.spines[axis].set_linewidth(3)

		graph.plot(data[0], data[1], color='#2da9b9', linewidth=2, marker='.', linestyle='-')

		# Hover animation
		def show_annotation(sel):
			_, y = sel.target
			sel.annotation.set_text(f"{y:.3f}")
		cursor = mplcursors.cursor(graph, hover=True)
		cursor.connect('add', show_annotation)

		self.canvas.draw()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyleSheet(open("styles.qss").read())
	ex = Window()
	sys.exit(app.exec_())
