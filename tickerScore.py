from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import pickle
import os.path



api_key = ""
api_secret = ""

client = Client(api_key, api_secret)


# get historical kline data from any date range


def save(name, data):
    f = open(name, 'wb')
    pickle.dump(data, f)
    f.close()

def load(name):
    f = open(name, 'rb')
    data = pickle.load(f)
    f.close()
    return data







OPEN_TIME = 0
OPEN = 1
HIGH = 2
LOW = 3
CLOSE = 4
VOLUME = 5
CLOSE_TIME = 6
QUOTE_ASSET_VOLUME = 7
NUMBER_TRADES = 8
TAKER_BASE_ASSET_VOLUME = 9
TAKER_QUOTE_ASSET_VOLUME = 10

class Candle:
    def __init__(self, candleData):
        self.open_time = candleData[OPEN_TIME]
        self.open = float(candleData[OPEN])
        self.high = float(candleData[HIGH])
        self.low = float(candleData[LOW])
        self.close = float(candleData[CLOSE])
        self.volume = float(candleData[VOLUME])
        self.close_time = candleData[CLOSE_TIME]
        self.quote_asset_volume = float(candleData[QUOTE_ASSET_VOLUME])
        self.number_of_trades = candleData[NUMBER_TRADES]



def getKlines(ticker:str):
    file = "candles/"+ticker
    if os.path.isfile(file):
        return load(file)
    else:
        # fetch 1 minute klines for the last day up until now
        klines = client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
        candles = []
        for kline in klines:
            candles.append(Candle(kline))
        save(file, candles)
        return candles

def getAllTickers():
    name = "All Tickers"
    if os.path.isfile(name):
        return load(name)
    else:
        # fetch 1 minute klines for the last day up until now
        tickersData = client.get_all_tickers()
        tickers = []
        for ticker in tickersData:
            tickers.append(ticker['symbol'])
        save(name, tickers)
        return tickers





def frequencyOfDeltas(candles):
    histogram = {}
    
    for candle in candles:
        delta = candle.open - candle.close
        percent = delta/float(candle.high) * 100
        percent = int(percent*10)/10
        if not percent in histogram:
             histogram[percent] = 0

        histogram[percent] += 1
    return histogram    

def plotHistogram(histogram):
    import plotille
    import numpy as np

    X = [1,1,1,1,2,2,3]

    fig = plotille.Figure()
    fig.width = 60
    fig.height = 30
    fig.color_mode = 'byte'

    data = []
    for key in histogram:
        for i in range(0, histogram[key]):
            data.append(key)

    bins = histogram.keys().__len__()

    fig.histogram(
        data,
        bins=bins
    )

    print(fig.show(legend=True))







def percentAbove(histogram, threshold):
    total = 0
    amountAbove = 0
    for percent in histogram:
        total += histogram[percent]
        if(percent > threshold):
            amountAbove += histogram[percent]
    if(total == 0):
        return 0
    return amountAbove/total

def flipHisto(histogram):
    newHisto = {}
    for percent in histogram:
        newHisto[-percent] = histogram[percent]
    return newHisto


def totalTrades(candles):
    total = 0
    for candle in candles:
        total+=candle.number_of_trades
    return total


def analyseTicker(ticker):
   
    candles = getKlines(ticker)
    histogram = frequencyOfDeltas(candles)
   
    upPercent = percentAbove(histogram, 1)
    downPercent = percentAbove(flipHisto(histogram), 1)

    if(downPercent == 0 or upPercent == 0):
        return
    if(1/ upPercent / 60 < 0.5 or 1/ downPercent / 60 < 0.5):
        print(ticker)
        print(histogram)
        if(upPercent == 0):
            print(0)
        else:
            print(1/upPercent/60)
        if(downPercent == 0):
            print(0)
        else:
            print(1/downPercent/60)
    
        trades = totalTrades(candles)
        print(trades/60)

        print()




tickers = getAllTickers()
print(len(tickers))
tickers = tickers

for ticker in tickers:
    analyseTicker(ticker)