from backtesting import Backtest, Strategy 
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG
import talib
import yfinance as yf
import datetime as dt
import pandas as pd
import numpy as np

ticker = "NVDA"
start = dt.datetime(2023, 1, 1)
end = dt.datetime(2025, 1, 1)
data = yf.download(ticker, start=start, end=end, group_by="column", auto_adjust=False)
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)  
    data.columns.name = None
data = data[['Open', 'High', 'Low', 'Close', 'Volume']]

class SMAStrategy(Strategy):

    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA,price,10)
        self.ma2 = self.I(SMA,price,20)
    
    def next(self):
        if crossover(self.ma1,self.ma2):
            self.buy()
        elif crossover(self.ma2,self.ma1):
            self.sell()


class MACDStrategy(Strategy):
    
    def init(self):
        price = self.data.Close
        self.macd =  self.I(lambda x: talib.MACD(x)[0],price)
        self.macd_signal =  self.I(lambda x: talib.MACD(x)[1],price)

    def next(self):
        if crossover(self.macd,self.macd_signal):
            self.buy()
        elif crossover(self.macd_signal,self.macd):
            self.sell()

class RSIStrategy(Strategy):
    def init(self):
        price = self.data.Close
        self.rsi = self.I(talib.RSI, price, 14)
    
    def next(self):
        if self.rsi[-1] < 30: 
            self.buy()
        elif self.rsi[-1] > 70: 
            self.sell()


class BollingerBandsStrategy(Strategy):
    def init(self):
        price = self.data.Close
        self.upper, self.middle, self.lower = self.I(
            talib.BBANDS, price, timeperiod=20, nbdevup=2, nbdevdn=2
        )
    
    def next(self):
        price = self.data.Close[-1]
        if price < self.lower[-1]:  
            self.buy()
        elif price > self.upper[-1]:  
            self.sell()


class MAATRStrategy(Strategy):
    def init(self):
        price = self.data.Close
        self.ma = self.I(SMA, price, 50)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, price, 14)
    
    def next(self):
        price = self.data.Close[-1]
        if price > self.ma[-1]:
            self.buy(sl=price - 2 * self.atr[-1])
        elif price < self.ma[-1]:
            self.sell()


class VWAPStrategy(Strategy):
    def init(self):
        typical_price = (self.data.High + self.data.Low + self.data.Close) / 3
        self.vwap = self.I(
            lambda tp, vol: np.cumsum(tp * vol) / np.cumsum(vol),
            typical_price, self.data.Volume
        )
    
    def next(self):
        if self.data.Close[-1] > self.vwap[-1]:
            self.buy()
        else:
            self.sell()


class DualMA_MACDStrategy(Strategy):
    def init(self):
        price = self.data.Close
        self.ma_fast = self.I(SMA, price, 10)
        self.ma_slow = self.I(SMA, price, 50)
        self.macd_line = self.I(lambda x: talib.MACD(x)[0], price)
    
    def next(self):
     
        if crossover(self.ma_fast, self.ma_slow) and self.macd_line[-1] > 0:
            self.buy()
   
        elif crossover(self.ma_slow, self.ma_fast) and self.macd_line[-1] < 0:
            self.sell()




strategies = {
    "SMA Crossover": SMAStrategy,
    "MACD": MACDStrategy,
    "RSI Mean Reversion": RSIStrategy,
    "Bollinger Bands": BollingerBandsStrategy,
    "MA + ATR Stop": MAATRStrategy,
    "VWAP": VWAPStrategy,
    "Dual MA + MACD Filter": DualMA_MACDStrategy
}

results = {}
for name, strategy in strategies.items():
    bt = Backtest(data, strategy, commission=0.002, exclusive_orders=True)
    results[name] = bt.run()
    print(f"\n{name} Strategy Results:")
    print(results[name])
    bt.plot()