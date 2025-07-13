import datetime as dt
from typing import Dict, List, Type
from main import strategies, data
from backtesting import Backtest
import pandas as pd
from tabulate import tabulate
import yfinance as yf
import matplotlib.pyplot as plt


STRATEGY_CODES = {
    'SMA': 'SMA Crossover',
    'MACD': 'MACD',
    'RSI': 'RSI Mean Reversion',
    'BB': 'Bollinger Bands',
    'MAATR': 'MA + ATR Stop',
    'VWAP': 'VWAP',
    'DMA': 'Dual MA + MACD Filter'
}

def display_welcome():
   
    print("\n" + "="*50)
    print("QUANTITATIVE TRADING STRATEGY BACKTESTER")
    print("="*50 + "\n")
    
    
    strategy_table = []
    for code, full_name in STRATEGY_CODES.items():
        strategy_table.append([code, full_name])
    
    print("Available Strategies:")
    print(tabulate(strategy_table, 
                 headers=["Code", "Strategy Name"],
                 tablefmt="grid"))
    print("\nEnter strategy codes separated by commas (e.g., 'SMA,MACD,RSI')")

def get_user_input(prompt: str, default=None, input_type=str):

    while True:
        user_input = input(f"{prompt} [{default}]: " if default else f"{prompt}: ")
        if not user_input and default is not None:
            return default
        try:
            return input_type(user_input)
        except ValueError:
            print(f"Invalid input. Please enter a {input_type.__name__}.")

def run_backtest(strategy_name: str, strategy_class: Type, data: pd.DataFrame, 
                 commission: float = 0.002, cash: float = 10000) -> Dict:
  
    bt = Backtest(data, strategy_class, commission=commission, cash=cash)
    results = bt.run()
    return {
        'strategy': strategy_name,
        'results': results,
        'backtest': bt
    }

def display_single_strategy(results: Dict):
    
    res = results['results']
    
  
    summary = [
        ["Return %", f"{res['Return [%]']:.2f}"],
        ["Annual Return %", f"{res['Return (Ann.) [%]']:.2f}"],
        ["Max Drawdown %", f"{res['Max. Drawdown [%]']:.2f}"],
        ["Sharpe Ratio", f"{res['Sharpe Ratio']:.2f}"],
        ["Win Rate %", f"{res['Win Rate [%]']:.2f}"],
        ["# Trades", res['# Trades']],
        ["Profit Factor", f"{res['Profit Factor']:.2f}"],
        ["Buy & Hold Return %", f"{res['Buy & Hold Return [%]']:.2f}"]
    ]
    
    print("\n" + "="*50)
    print(f"{results['strategy']} Results")
    print("="*50)
    print(tabulate(summary, tablefmt="grid"))
    

    results['backtest'].plot()
    plt.show()

def compare_strategies(results_list: List[Dict]) -> pd.DataFrame:
   
    comparison = []
    
    for result in results_list:
        res = result['results']
        comparison.append({
            'Strategy': result['strategy'],
            'Return %': res['Return [%]'],
            'Ann. Return %': res['Return (Ann.) [%]'],
            'Max DD %': res['Max. Drawdown [%]'],
            'Sharpe': res['Sharpe Ratio'],
            'Win Rate %': res['Win Rate [%]'],
            '# Trades': res['# Trades'],
            'Profit Factor': res['Profit Factor']
        })
    
    df = pd.DataFrame(comparison).set_index('Strategy')
    return df

def main():
    display_welcome()
    

    while True:
        strategy_input = get_user_input(
            "Enter strategy code(s)", 
            default="SMA,MACD,RSI"
        ).upper()
        
        selected_strategies = []
        invalid_strategies = []
        
        for code in strategy_input.split(','):
            code = code.strip()
            if code in STRATEGY_CODES:
                selected_strategies.append(STRATEGY_CODES[code])
            else:
                invalid_strategies.append(code)
        
        if invalid_strategies:
            print(f"Invalid strategy codes: {', '.join(invalid_strategies)}")
            continue
        
        if not selected_strategies:
            print("Please select at least one valid strategy.")
            continue
            
        break
    
    ticker = get_user_input("Enter ticker symbol", default="NVDA")
    start_date = get_user_input(
        "Start date (YYYY-MM-DD)", 
        default="2023-01-01",
        input_type=lambda s: dt.datetime.strptime(s, '%Y-%m-%d')
    )
    end_date = get_user_input(
        "End date (YYYY-MM-DD)", 
        default="2025-01-01",
        input_type=lambda s: dt.datetime.strptime(s, '%Y-%m-%d')
    )
    commission = get_user_input(
        "Commission rate", 
        default=0.002,
        input_type=float
    )
    initial_cash = get_user_input(
        "Initial capital", 
        default=10000,
        input_type=float
    )
    

    print(f"\nDownloading {ticker} data from {start_date} to {end_date}...")
    data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)  
        data.columns.name = None
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
    

    results_list = []
    for strategy_name in selected_strategies:
        print(f"\nRunning {strategy_name} backtest...")
        results = run_backtest(
            strategy_name,
            strategies[strategy_name],
            data,
            commission,
            initial_cash
        )
        results_list.append(results)
    

    if len(results_list) == 1:
        display_single_strategy(results_list[0])
    else:
        print("\n" + "="*50)
        print("STRATEGY COMPARISON")
        print("="*50)
        
        df = compare_strategies(results_list)
        
        
        format_dict = {
            'Return %': '{:.2f}%',
            'Ann. Return %': '{:.2f}%',
            'Max DD %': '{:.2f}%',
            'Sharpe': '{:.2f}',
            'Win Rate %': '{:.2f}%',
            'Profit Factor': '{:.2f}'
        }
        
        styled_df = df.style.format(format_dict)
        print(styled_df.to_string())
        
        
        ax = df[['Return %', 'Ann. Return %']].plot(kind='bar', figsize=(10, 6))
        ax.set_title('Strategy Performance Comparison')
        ax.set_ylabel('Return (%)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    
    main()