from datetime import datetime
from datetime import date
import numpy as np

import pandas as pd
now = datetime.today().date()
# now = datetime.strptime('2018-01-15','%Y-%m-%d').date()
if(bool(len(pd.bdate_range(now,now)))):
    pass

def calculate_sma(stock, window_slow=30, window_fast=20):
    stock['fast_rolling'] = stock.Close.rolling(window=window_fast).mean()
    stock['slow_rolling'] = stock.Close.rolling(window=window_slow).mean()
    stock['diff'] = stock['slow_rolling'] - stock['fast_rolling']
    n_row = stock.shape[0]
    action = ['no'] * n_row
    for i in range(0, n_row):
        if stock['diff'][i] > 0 and stock['diff'][i-1] <= 0:
            action[i] = "buy"
        if stock['diff'][i] < 0 and stock['diff'][i-1] >= 0:
            action[i] = "sell"
    stock['action'] = action
    return stock

if __name__ == '__main__':
    from hist_stock_data import get

    stock = get('2017-01-01', '2018-01-01', 'AAPL')
    stock_sma = calculate_sma(stock, 20, 10)
    print(stock_sma.tail())
