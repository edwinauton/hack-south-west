import sys
from functools import partial

import matplotlib.pyplot as plt
import mplcursors
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QGridLayout, QScrollArea, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QFrame
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import utils


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
        self.stocks_owned = QLabel()
        self.stocks = list()
        self.init()

    def init(self):
        # Table Header
        header = QHBoxLayout()

        spacer = utils.create_label("")
        header.addWidget(spacer)

        price = utils.create_label("Price")
        price.setObjectName("subheading")
        header.addWidget(price)

        change = utils.create_label("Change")
        change.setObjectName("subheading")
        header.addWidget(change)

        equity = utils.create_label("Equity")
        equity.setObjectName("subheading")
        header.addWidget(equity)

        daily_return = utils.create_label("Return")
        daily_return.setObjectName("subheading")
        header.addWidget(daily_return)

        header.addWidget(spacer)
        header.addWidget(spacer)

        stocks_owned = utils.create_label("Stocks Owned")
        stocks_owned.setObjectName("subheading")
        header.addWidget(stocks_owned)

        self.table.addLayout(header)
        self.table.addWidget(utils.create_line())

        # Add spacing after heading
        self.table.insertSpacing(1, 10)
        self.table.addWidget(utils.create_line())

        self.stocks = utils.get_stocks_list()

        for stock in self.stocks:
            # Setup Row
            row = QHBoxLayout()

            # Ticker Button
            self.ticker = utils.create_button(str(stock.ticker))
            self.ticker.clicked.connect(partial(self.update_graph, stock))
            row.addWidget(self.ticker)

            # Last Price
            value = utils.format(stock.start_price)
            self.last_price = utils.create_label(value)
            row.addWidget(self.last_price)

            # Change
            value = utils.format(stock.change)
            self.change = utils.create_label(value)
            utils.colour(self.change)
            row.addWidget(self.change)

            # Equity
            value = utils.format(stock.equity)
            self.equity = utils.create_label(value)
            row.addWidget(self.equity)

            # Daily Return
            value = utils.format(stock.daily_return)
            self.daily_return = utils.create_label(value)
            utils.colour(self.daily_return)
            row.addWidget(self.daily_return)

            self.stocks_owned = utils.create_label(str(stock.number_owned))

            # Buy Button
            self.buy_button = utils.create_button("Buy")
            self.buy_button.clicked.connect(partial(self.update_stocks, 1, stock))
            row.addWidget(self.buy_button)

            # Sell Button
            self.sell_button = utils.create_button("Sell")
            self.sell_button.clicked.connect(partial(self.update_stocks, -1, stock))
            row.addWidget(self.sell_button)

            # Stocks Owned
            row.addWidget(self.stocks_owned)
            self.table.addLayout(row)
            self.table.addWidget(utils.create_line())

        # Setup Grid
        layout = QGridLayout()

        # Titles
        value = utils.format(round(sum(stock.equity for stock in self.stocks), 2))
        self.portfolio_value = utils.create_label(f"Portfolio Value: {value}")
        self.portfolio_value.setObjectName("heading")
        layout.addWidget(self.portfolio_value, 0, 1, 1, 1)
        value = utils.format(round(sum(stock.daily_return for stock in self.stocks), 2))
        self.overall_return = utils.create_label(f"Today's Return: {value}")
        utils.colour_heading(self.overall_return)
        layout.addWidget(self.overall_return, 1, 1, 1, 1)

        # Scrollable Table
        self.widget.setLayout(self.table)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.scroll.setFrameShape(QFrame.NoFrame)
        layout.addWidget(self.scroll, 0, 3, 3, 1)

        # Graph
        layout.addWidget(self.canvas, 2, 0, 1, 3)
        self.plot_graph((self.stocks[0].create_graph()[0], sum(stock.create_graph()[1] for stock in self.stocks)))

        # Window Properties
        self.setWindowTitle("Stock Trading Simulator")
        self.setWindowIcon(QIcon("styles/icon.jpg"))
        self.setGeometry(10, 10, 2560, 1440)
        self.setMinimumSize(1500, 900)
        self.setLayout(layout)
        self.show()

    def update_graph(self, stock):
        self.plot_graph(stock.create_graph())
        self.update()

    def update_stocks(self, value, stock):
        stock.number_owned += value

        """
		# Convert data to dictionary
		data = dict()
		for stock in self.stocks:
			data.update({stock.ticker: stock.number_owned})

		# Save stocks information to file
		with open("stock_record.json") as f:
			json.dump(data, f)

		self.update()
		"""

    def plot_graph(self, data):
        # Setup figure to plot graph
        self.figure.clear()
        graph = self.figure.add_subplot(111)

        # Hide x-axis and recolour y-axis text and ticks
        graph.xaxis.set_visible(False)
        graph.yaxis.label.set_color("#2da9b9")
        graph.tick_params(axis="y", colors="#2da9b9")

        # Recolour and resize graph borders
        for axis in ["top", "bottom", "left", "right"]:
            graph.spines[axis].set_color("#2da9b9")
            graph.spines[axis].set_linewidth(3)

        # Plot data, using a coloured line
        graph.plot(data[0], data[1], color="#2da9b9", linewidth=2, marker=".", linestyle="-")

        # Hover animation
        def show_annotation(sel):
            _, y = sel.target
            sel.annotation.set_text(f"{y:.2f}")

        cursor = mplcursors.cursor(graph, hover=True)
        cursor.connect("add", show_annotation)

        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Use QSS style sheets
    app.setStyleSheet(open("styles/styles.qss").read())

    ex = Window()
    sys.exit(app.exec_())
