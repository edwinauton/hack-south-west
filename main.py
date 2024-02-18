import json
import sys
from functools import partial

import matplotlib.pyplot as plt
import mplcursors
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QGridLayout, QScrollArea, QWidget, QHBoxLayout, QVBoxLayout, QFrame
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import gui_utils as utils


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.table = QVBoxLayout()
        self.stocks = list()
        self.portfolio_value = QLabel()
        self.overall_return = QLabel()
        self.vbox = QVBoxLayout()

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
        header.setContentsMargins(10, 10, 25, 10)

        self.vbox.addLayout(header)

        # Add spacing after header
        self.vbox.addWidget(utils.create_line())
        self.vbox.insertSpacing(1, 5)
        self.vbox.addWidget(utils.create_line())

        self.stocks = utils.get_stocks_list()

        for stock in self.stocks:
            # Ticker Button
            ticker = utils.create_button(stock.ticker)
            ticker.clicked.connect(partial(self.update_graph, stock))

            # Last Price
            value = utils.format(stock.start_price)
            last_price = utils.create_label(value)

            # Change
            value = utils.format(stock.change)
            change = utils.create_label(value)
            utils.colour(change)

            # Equity
            value = utils.format(stock.equity)
            equity = utils.create_label(value)

            # Daily Return
            value = utils.format(stock.daily_return)
            daily_return = utils.create_label(value)
            utils.colour(daily_return)

            stocks_owned = utils.create_label(stock.number_owned)

            # Buy Button
            buy_button = utils.create_button("Buy")
            buy_button.clicked.connect(partial(self.update_stock, 1, stock, equity, daily_return, stocks_owned))

            # Sell Button
            sell_button = utils.create_button("Sell")
            sell_button.clicked.connect(partial(self.update_stock, -1, stock, equity, daily_return, stocks_owned))

            # Setup and add cells to row
            row = QHBoxLayout()
            row.addWidget(ticker)
            row.addWidget(last_price)
            row.addWidget(change)
            row.addWidget(equity)
            row.addWidget(daily_return)
            row.addWidget(buy_button)
            row.addWidget(sell_button)
            row.addWidget(stocks_owned)

            self.table.addLayout(row)
            self.table.addWidget(utils.create_line())

        # Setup Grid
        layout = QGridLayout()

        # Titles
        value = utils.format(self.calculate_total_equity())
        self.portfolio_value = utils.create_label(f"\n\nPortfolio Value: {value}")
        self.portfolio_value.setObjectName("heading")
        layout.addWidget(self.portfolio_value, 0, 1, 1, 1)
        value = utils.format(self.calculate_overall_return())
        self.overall_return = utils.create_label(f"\nToday's Return: {value}")
        utils.colour(self.overall_return)
        layout.addWidget(self.overall_return, 1, 1, 1, 1)

        # Scrollable Table
        self.widget.setLayout(self.table)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.vbox.addWidget(self.scroll)
        layout.addLayout(self.vbox, 0, 3, 3, 1)

        # Graph
        layout.addWidget(self.canvas, 2, 0, 1, 3)
        self.plot_graph((self.stocks[0].create_graph()[0], sum(stock.create_graph()[1] for stock in self.stocks)))

        # Window Properties
        self.setWindowTitle("Stock Trading Simulator")
        self.setWindowIcon(QIcon("styles/icon.jpg"))
        self.setGeometry(10, 10, 2560, 1440)
        self.setMinimumSize(1600, 900)
        self.setLayout(layout)
        self.show()

    # Function to update the graph being shown
    def update_graph(self, stock):
        self.plot_graph(stock.create_graph())
        self.update()

    # Function to update all values changed when a stock is sold/bought
    def update_stock(self, value, stock, equity, daily_return, stocks_owned):
        if stock.number_owned > 0 or value == 1:
            stock.number_owned += value
            stocks_owned.setText(str(stock.number_owned))
            stock.update()
            equity.setText(str(stock.equity))
            daily_return.setText(str(stock.daily_return))

            value = utils.format(self.calculate_total_equity())
            self.portfolio_value.setText(f"\n\nPortfolio Value: {value}")
            value = utils.format(self.calculate_overall_return())
            self.overall_return.setText(f"\nToday's Return: {value}")
            utils.colour(self.overall_return)

    # Function to plot and stylise graph
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
        graph.plot(data[0], data[1], color="#2da9b9", linewidth=2, marker="", linestyle="-")

        # Hover animation
        def show_annotation(sel):
            _, y = sel.target
            sel.annotation.set_text(f"{y:.2f}")

        cursor = mplcursors.cursor(graph, hover=True)
        cursor.connect("add", show_annotation)

        self.canvas.draw()

    # Function to calculate total portfolio value
    def calculate_total_equity(self):
        return round(sum(stock.equity for stock in self.stocks), 2)

    # Function to calculate total income for the day
    def calculate_overall_return(self):
        return round(sum(stock.daily_return for stock in self.stocks), 2)

    # Function which runs when the program is closed; saves stocks to a file
    def closeEvent(self, event):
        # Convert data to dictionary
        data = dict()
        for stock in self.stocks:
            data.update({stock.ticker: stock.number_owned})

        # Save stocks information to file
        with open("stock_record.json", "w") as f:
            json.dump(data, f)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Use QSS style sheets
    app.setStyleSheet(open("styles/styles.qss").read())

    window = Window()
    sys.exit(app.exec_())
