import pandas as pd
from ma_2_line import MovingAvg
from stock_ticker_list import get_sp500_tickers
import time

tickers = get_sp500_tickers()[5:10]
# sma = MovingAvg(start_date='2017-01-01',
#                 end_date='2018-01-06',
#                 ticker='SPY',
#                 price_type='Close',
#                 slow_window=15,
#                 fast_window=8,
#                 cash_input=10000)
# sma.get_stock()
# sma.get_sma()
# sma.plot_sma()
# profit= sma.get_sma_profit()
# profit

profits = list()
ticks = list()
for ticker in tickers:
    sma = MovingAvg(start_date='2017-01-01',
                    end_date='2018-01-01',
                    ticker=ticker,
                    price_type='Close',
                    slow_window=10,
                    fast_window=5,
                    cash_input=10000)
    profit = sma.get_sma_profit()
    p = list(profit['cash_total'])[-1]
    profits.append(p)
    print(ticker + " completed.")
    time.sleep(5)

#print(profits)
df = pd.DataFrame({'Ticker': tickers, 'Profit': profits})
print(df)
