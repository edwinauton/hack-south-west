import requests
import json
from os import getenv
from dotenv import load_dotenv
load_dotenv()
url = "https://alphavantage.co/query"
def makeRequest(function, symbol, interval, month):
    params = {
        "function": function,
        "symbol": symbol,
        "interval": interval,
        "month" : month,
        "apikey": "3ER47V2K5KWDABOO"
    }
    print(params)
    response = requests.get(url, params=params)
    return response

def getDailyData(symbol : str, month : str) -> json:
    '''
    Gets stock data in 1 hour intervals for a given month
    :param symbol: stock ticker
    :param month: format YYYY-MM
    :return: json
    '''

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "interval": "60min",
        "apikey": getenv("api_key"),
        "month" : month,
        "outputsize": "full"
    }
    return requests.get(url, params=params).json()

def getHourlyData(symbol : str, month : str) -> json:
    '''
    Gets stock data in 5 min intervals for a given day
    :param symbol:
    :param day:
    :return:
    '''

    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "5min",
        "apikey": getenv("api_key"),
        "month" : month,
        "outputsize": "full"

    }

    return requests.get(url, params=params).json()



