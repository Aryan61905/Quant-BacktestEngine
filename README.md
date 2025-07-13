# Quant-Backtest Script

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Backtesting.py](https://img.shields.io/badge/Backtesting.py-0.3.3-green)
![TA-Lib](https://img.shields.io/badge/TA--Lib-0.4.24-yellow)

## Strategies:

A comprehensive backtesting framework for evaluating 7 different quantitative trading strategies

```bash
SMA Crossover (10/20)
MACD (12/26/9)
RSI Mean Reversion (30/70)
Bollinger Bands (20,2σ)
MA + ATR Stop (50 SMA, 2xATR)
VWAP Trend FollowingDual 
MA + MACD Filter (10/50)
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Aryan61905/Quant-BacktestEngine.git
   cd Quant-BacktestEngine
   ```
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   ```makefile
   requirements.txt:
   backtesting==0.3.3
   numpy>=1.20.0
   pandas>=1.2.0
   yfinance>=0.1.70
   TA-Lib>=0.4.24
   ```

## Usage

1. Modify the stock ticker and date range in `main.py`:

   ```python
   # Modify as per requirement
   ticker = "NVDA"  
   start = dt.datetime(2023, 1, 1)
   end = dt.datetime(2025, 1, 1)
   ```
2. Run the backtest:

   ```bash
   python main.py
   ```

## What is Backtesting?

Backtesting is the process of testing a trading strategy using historical market data to evaluate how it would have performed in the past. It helps traders and quants:

* Assess profitability and risk
* Fine-tune parameters
* Validate ideas before risking real capital

In essence, if a strategy performs well historically, it may perform well in live markets — though past performance doesn't guarantee future results.


### 1. SMA Crossover Strategy

* Uses two Simple Moving Averages (10-day and 20-day)
* Generates buy signal when fast MA (10-day) crosses above slow MA (20-day)
* Generates sell signal when fast MA crosses below slow MA
* Classic trend-following approach

### 2. MACD Strategy

* Implements Moving Average Convergence Divergence indicator
* Buys when MACD line crosses above signal line
* Sells when MACD line crosses below signal line
* Captures momentum shifts in the market

### 3. RSI Mean Reversion Strategy

* Uses Relative Strength Index (14-period)
* Buys when RSI falls below 30 (oversold condition)
* Sells when RSI rises above 70 (overbought condition)
* Attempts to profit from price returning to mean

### 4. Bollinger Bands Strategy

* Tracks price relative to volatility bands
* Buys when price touches lower band
* Sells when price touches upper band
* Combines mean reversion with volatility assessment

### 5. MA + ATR Stop Strategy

* Uses 50-day moving average as trend filter
* Implements Average True Range (ATR) for stop-loss
* Buys when price above MA with 2x ATR stop
* Sells when price below MA
* Manages risk with volatility-based stops

### 6. VWAP Strategy

* Tracks Volume Weighted Average Price
* Buys when price above VWAP (bullish momentum)
* Sells when price below VWAP (bearish momentum)
* Incorporates both price and volume data

### 7. Dual MA + MACD Filter Strategy

* Combines two concepts:

  * 10-day/50-day MA crossover
  * MACD line as confirmation filter
* Only trades in direction of MACD sign
* Reduces false signals with multiple confirmations

  ## Results:


  1. **Start/End/Duration** : Test period timeframe and total days analyzed
  2. **Exposure Time** : Percentage of time the strategy held positions
  3. **Equity Final** : Ending portfolio value after all trades
  4. **Equity Peak** : Highest portfolio value reached
  5. **Commissions** : Total trading fees paid
  6. **Return** : Net profit/loss percentage
  7. **Buy & Hold Return** : Benchmark performance without trading
  8. **Return (Ann.)** : Annualized return percentage
  9. **Volatility (Ann.)** : Annualized standard deviation of returns
  10. **CAGR** : Compound annual growth rate
  11. **Sharpe Ratio** : Risk-adjusted returns (higher=better)
  12. **Sortino Ratio** : Downside risk-adjusted returns
  13. **Calmar Ratio** : Return relative to max drawdown
  14. **Alpha** : Excess return vs market (positive=outperformance)
  15. **Beta** : Portfolio volatility vs market
  16. **Max Drawdown** : Largest peak-to-trough loss
  17. **Avg Drawdown** : Average losing period severity
  18. **Max Drawdown Duration** : Longest recovery time from losses
  19. **Avg Drawdown Duration** : Typical recovery time
  20. **# Trades** : Total executed transactions
  21. **Win Rate** : Percentage of profitable trades
  22. **Best/Worst Trade** : Most/least profitable single trade
  23. **Avg Trade** : Mean return per trade
  24. **Trade Duration** : Time held per position
  25. **Profit Factor** : Gross profits ÷ gross losses
  26. **Expectancy** : Average return per trade
  27. **SQN** : System Quality Number (strategy confidence)
  28. **Kelly Criterion** : Optimal position sizing percentage
