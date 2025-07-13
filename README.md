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
