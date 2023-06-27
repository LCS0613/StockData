import pandas as pd
import yfinance as yf
import investpy

def kospi_ticker():

    # 한국 주식 상장 목록 불러오기
    kospi_data = investpy.get_stocks(country='South Korea')
    kospi_data = kospi_data.loc[:, ['symbol', 'name']]
    kospi_data.columns = ['Ticker', 'Name']

    return kospi_data

def nasdaq_ticker():
    # 미국 주식 상장 목록 불러오기
    nasdaq_data = investpy.get_stocks(country='United States')
    nasdaq_data = nasdaq_data.loc[:, ['symbol', 'name']]
    nasdaq_data.columns = ['Ticker', 'Name']

    return nasdaq_data

def get_stock_information(tickers):
    stock_information = []
    for ticker in tickers:
        stock_info = yf.Ticker(ticker).info
        stock_information.append([stock_info['symbol'], stock_info.get('shortName', None),
                                  stock_info.get('trailingPE', None),
                                  stock_info.get('enterpriseToEbitda', None), stock_info.get('priceToBook', None),
                                  stock_info.get('priceToSales', None), stock_info.get('enterpriseToRevenue', None),
                                  stock_info.get('forwardPE', None), stock_info.get('trailingEps', None),
                                  stock_info.get('roe', None)])

    columns = ['symbol', 'name', 'p/e', 'ev/ebitda', 'p/b', 'p/s', 'ev/revenue', 'forward p/e', 'eps', 'roe']
    stock_information_df = pd.DataFrame(stock_information, columns=columns)

    print(stock_information_df)


if __name__ == '__main__':
    print(kospi_ticker())
    print(nasdaq_ticker())
    print(get_stock_information(['AAPL', 'MSFT']))
