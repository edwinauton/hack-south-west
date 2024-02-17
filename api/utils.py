import requests

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

def getDailyData(symbol, month):
    response = makeRequest("TIME_SERIES_DAILY", symbol, "5min", month)
    data = response.json()
    return data


def getHourlyData(symbol, month):
    response = makeRequest("TIME_SERIES_INTRADAY", symbol, "5min", month)
    data = response.json()
    return data


