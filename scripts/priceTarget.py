import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
from termcolor import colored

def get_analyst_price_targets(ticker):
    stock = yf.Ticker(ticker)
    analyst_info = stock.analyst_price_targets
    return analyst_info
    
def format_price_target(current_price, target_dict):

    if not target_dict:
        return "No data"
    
    upside_pct = ((target_dict['mean'] - current_price) / current_price) * 100
    color = 'green' if upside_pct > 15 else 'yellow' if upside_pct > 0 else 'red'
    
    return colored(
        f"{target_dict['mean']:.2f} ({upside_pct:+.1f}%)", 
        color,
        attrs=['bold']
    )


tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA"]


current_prices = {t: yf.Ticker(t).history(period='1d')['Close'].iloc[-1] for t in tickers}


analysis_data = []
for ticker in tickers:
    targets = get_analyst_price_targets(ticker)
    if targets:
        color = 'green' if current_prices[ticker] > targets.get('median', 'N/A') else 'red'
        row = {
            'Ticker': ticker,
            'Current': colored(
            f"{current_prices[ticker]:.2f}", 
            color,
            attrs=['bold']
            ),
            'Median Target': targets.get('median', 'N/A'),
            'Mean Target': targets.get('mean', 'N/A'),
            'Upside': format_price_target(current_prices[ticker], targets),
            'High': targets.get('high', 'N/A'),
            'Low': targets.get('low', 'N/A')
        }
        analysis_data.append(row)


print("\n" + "="*60)
print(colored(" ANALYST PRICE TARGETS SUMMARY ", 'white', 'on_blue', attrs=['bold']))
print("="*60)
print(tabulate(
    pd.DataFrame(analysis_data),
    headers='keys',
    tablefmt='fancy_grid',
    floatfmt=".2f",
    showindex=False
))


plt.figure(figsize=(12, 6))
df = pd.DataFrame(analysis_data)
df['Upside%'] = ((df['Mean Target'] - df['Current']) / df['Current']) * 100
df = df.sort_values('Upside%', ascending=False)

colors = ['green' if x > 0 else 'red' for x in df['Upside%']]
plt.bar(df['Ticker'], df['Upside%'], color=colors)
plt.axhline(0, color='black', linestyle='--')
plt.title('Analyst Price Target Upside Potential (%)', fontweight='bold')
plt.xlabel('Ticker')
plt.ylabel('Upside %')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle=':')
plt.tight_layout()
plt.show()
