import requests
from os import getenv
from dotenv import load_dotenv
load_dotenv()

url = "https://alphavantage.co/query"
if (getenv("api_key") == None):
    print("No API key found. Please set an environment variable")

def makeRequest(function, symbol, interval, month):
    params = {
        "function": function,
        "symbol": symbol,
        "interval": interval,
        "month" : month,
        "apikey": getenv("api_key")
    }
    print(params)
    response = requests.get(url, params=params)
    return response

def getDailyData(symbol, month):
    response = makeRequest("TIME_SERIES_DAILY", symbol, "5min", month)
    data = response.json()
    return data


def getHourlyData(symbol, month):
    response = makeRequest("TIME_SERIES_INTRADAY", symbol, "5min", month)
    data = response.json()
    return data


