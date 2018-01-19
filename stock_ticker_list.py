import pandas as pd
sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

def get_sp500_tickers(url=sp500_url):
    file = pd.read_html(sp500_url)
    table = file[0]
    tickers = list(table[1:][0])
    return tickers

if __name__ == '__main__':
    tickers = get_sp500_tickers()
    print(tickers)