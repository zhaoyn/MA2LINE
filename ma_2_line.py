from datetime import date
import numpy as np

import pandas as pd
import pandas_datareader as pdr
from datetime import datetime
import matplotlib.pyplot as plt

# now = datetime.today().date()
# # now = datetime.strptime('2018-01-15','%Y-%m-%d').date()
# if(bool(len(pd.bdate_range(now,now)))):
#     pass
class MovingAvg(object):
    def __init__(self,
                 start_date,
                 end_date,
                 ticker,
                 price_type,
                 slow_window,
                 fast_window,
                 cash_input):
        self.start_date = start_date
        self.end_date = end_date
        self.ticker = ticker
        self.price_type = price_type
        self.slow_window = slow_window
        self.fast_window = fast_window
        self.cash_input = cash_input
        self.stock = None
        self.stock_sma = None
        self.profit = None

    def get_stock(self):
        _start = datetime.strptime(self.start_date, '%Y-%m-%d').date()
        _end = datetime.strptime(self.end_date, '%Y-%m-%d').date()
        self.stock = pdr.get_data_yahoo(self.ticker, _start, _end)
        return self.stock

    def get_sma(self):
        if self.stock is None:
            self.get_stock()
        self.stock_sma = pd.DataFrame(self.stock[self.price_type])
        self.stock_sma['fast_rolling'] = self.stock_sma[self.price_type].rolling(window=self.fast_window).mean()
        self.stock_sma['slow_rolling'] = self.stock_sma[self.price_type].rolling(window=self.slow_window).mean()
        self.stock_sma['diff'] = self.stock_sma['slow_rolling'] - self.stock_sma['fast_rolling']
        n_row = self.stock_sma.shape[0]
        action = ['no'] * n_row
        for i in range(0, n_row):
            if self.stock_sma['diff'][i] > 0 and self.stock_sma['diff'][i-1] <= 0:
                action[i] = "sell"
            if self.stock_sma['diff'][i] < 0 and self.stock_sma['diff'][i-1] >= 0:
                action[i] = "buy"
        self.stock_sma['action'] = action
        return self.stock_sma

    def get_sma_profit(self):
        if self.stock_sma is None:
            self.get_sma()
        action = self.stock_sma.loc[self.stock_sma['action'] != 'no']
        for i in range(0, action.shape[0]):
            if action['action'][0] == 'sell':
                action = action.drop(action.index[0])
            else:
                break

        i = 0
        flag = 0
        entry_date = []
        entry_price = []
        exit_date = []
        exit_price = []
        while i < action.shape[0]:
            if flag == 0 and action['action'][i] == 'buy':
                entry_date.append(str(action.index[i]))
                entry_price.append(action[self.price_type][i])
                flag = 1
            if flag == 1 and action['action'][i] == 'sell':
                exit_date.append(str(action.index[i]))
                exit_price.append(action[self.price_type][i])
                flag = 0
            i = i + 1
        if flag == 1:
            exit_date.append(str(self.stock_sma.index[-1]))
            exit_price.append(self.stock_sma[self.price_type][-1])
        #print(action)
        profit = pd.DataFrame({'entry_date': entry_date,
                               'entry_price': entry_price,
                               'exit_date': exit_date,
                               'exit_price': exit_price})

        quantities = []
        profit_amounts = []
        cash_total = []
        for i in range(0, profit.shape[0]):
            quantity = self.cash_input // profit['entry_price'][i]
            quantities.append(quantity)
            profit_amount = (profit['exit_price'][i] - profit['entry_price'][i]) * quantity
            profit_amounts.append(profit_amount)
            self.cash_input = self.cash_input + profit_amount
            cash_total.append(self.cash_input)
        profit['quantity'] = quantities
        profit['profit_amount'] = profit_amounts
        profit['cash_total'] = cash_total
        profit['ticker'] = self.ticker
        return profit

    def plot_sma(self):
        if self.stock_sma is None:
            self.get_sma()
        plt.figure()
        self.stock_sma[self.price_type].plot(style='k--')
        self.stock_sma.fast_rolling.plot(label='fast_' + str(self.fast_window) + '_Day_SMA')
        self.stock_sma.slow_rolling.plot(label='slow_' + str(self.slow_window) + '_Day_SMA')
        plt.legend(loc='best')

