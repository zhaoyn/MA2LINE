"""
hist_stock_data.py accepts a list of ticker or one txt file contains tickers, one start date, one end data as inputs
retrieves history stock data and save to a dataframe
"""

import pandas_datareader as pdr
from datetime import datetime
import pandas as pd

def get_stock(start,end,ticker):
    _start = datetime.strptime(start,'%Y-%m-%d').date()
    _end = datetime.strptime(end, '%Y-%m-%d').date()
    stock = pdr.get_data_googel(ticker,_start,_end)
    return stock

if __name__ == '__main__':
    aapl = get_stock('2017-01-01','2018-01-01','AAPL')
    print(aapl.head())