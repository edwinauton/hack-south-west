import getLiveData
import json
tickers = ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN", "NVDA"]
def saveData(date, timeframe, ticker, data):
    path = "../resources/"
    filename = date + "_" + timeframe + "_" + ticker + ".json"

    with open(path + filename, "w") as file:
        json.dump(data, file)


for ticker in tickers:
    for month in range(1, 13):
        YYYYMM = "2023-" + str(month).zfill(2)

        data = getData.getHourlyData(ticker, YYYYMM)
        saveData(YYYYMM, "hourly", ticker, data)
        print("Done with " + ticker + " for " + YYYYMM)






