import quandl

quandl.ApiConfig.api_key = 'XE5LrzNpF2MJxH7qcDbm'

aapl = quandl.get('WIKI/AAPL')
print(aapl.tail())