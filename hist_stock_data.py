"""
hist_stock_data.py accepts a list of ticker or one txt file contains tickers, one start date, one end data as inputs
retrieves history stock data and save to a dataframe
"""

import pandas as pd
import  pandas_datareader as pdr
import datetime


def get(start,end,tickers):
    pass

start = datetime.datetime(2017,1,1)
end=datetime.date.today()

apple = pdr.get_data_yahoo("AAPL")

type(apple)

print(apple.head())