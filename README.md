# Binace Ticker Reviewer

This script grabs all the tickers on binance, grabs the last 25hr of 1 minute candles, and outputs which have a high delta.

This is useful to find certain tickers to then run market making bots, such as HummingBot on. 

Note, requests are cached in /candles/ folder, and delete this folder to get up to date data. 
