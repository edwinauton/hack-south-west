import json
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QLabel, QSizePolicy, QFrame

from stock import Stock


# Function to create a button with the given text
def create_button(text):
    button = QPushButton()
    button.setText(str(text))
    return button


# Function to create a label with the given text
def create_label(text):
    label = QLabel(str(text))
    label.setAlignment(Qt.AlignCenter)
    label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
    return label


# Function to create a dividing horizontal line
def create_line():
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setObjectName("line")
    return line


# Function to add a $ sign in front of a value
def format(data):
    string = str(data)
    if string[0] == "-":
        return "-$" + string[1:]
    else:
        return "$" + string


# Function to colour regular loss/gain figures
def colour(label):
    if "-" in label.text():
        label.setObjectName("loss")
    else:
        label.setObjectName("gain")


# Function to colour main loss/gain figure
def colour_heading(heading):
    if "-" in heading.text():
        heading.setObjectName("heading_loss")
    else:
        heading.setObjectName("heading_gain")


# Function to create a list of stocks from a file
def get_stocks_list():
    # Read stocks stored in file
    with open("stock_record.json") as f:
        data = json.load(f)

    stocks_list = []

    # Read data from files provided by API
    for subdir, dirs, files in os.walk("resources"):
        for file in files:
            filepath = subdir + os.sep + file
            if file.endswith(".json"):
                filename = os.path.splitext(file)[0]
                try:
                    number_of_stocks = data[filename]
                except KeyError:
                    number_of_stocks = 0
                stocks_list.append(Stock(filepath, number_of_stocks))

    return stocks_list
