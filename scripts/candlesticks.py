import datetime as dt
import pandas_datareader as web
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf
import yfinance as yf
import pandas as pd

ticker = "NVDA"
start = dt.datetime(2025,1,1)
end = dt.datetime(2025,7,1)
data = yf.download(ticker, start=start, end=end, group_by="column", auto_adjust=False)

if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)
    
#OHLC
data = data[["Open","High","Low","Close"]]
data.index.name = 'Date'


mpf.plot(data,type = "candle", style='yahoo')



