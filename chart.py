import matplotlib.pyplot as plt
import yfinance as yf

class Chart:
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date

        # 데이터 가져오기
        self.data = yf.download(self.ticker, start=self.start_date, end=self.end_date)

    # 수익률 차트 플롯
    def plotreturn(self, type='month'):

        if type == 'day':
            # 일별 수익률 계산
            data_returns = self.data['Close'].pct_change()
        elif type == 'month':
            # 월별 수익률 계산
            data_returns = self.data['Close'].resample('M').ffill().pct_change()
        elif type == 'year':
            # 연별 수익률 계산
            data_returns = self.data['Close'].resample('Y').ffill().pct_change()
        else:
            raise ValueError('수익률을 계산할 단위(day, month, year)가 잘못 입력되었습니다.')

        # 수익률 그래프 그리기
        plt.figure(figsize=(12, 6))
        plt.plot(data_returns, label=self.ticker)
        plt.xlabel('Date')
        plt.ylabel('Returns')
        plt.title('Stock Returns' + '(' + type + ')')
        plt.legend()
        plt.show()

    def plotstock(self, type='month'):

        if type == 'day':
            plt.plot(self.data['Adj Close'], label=self.ticker)
        elif type == 'month':
            monthly_data = self.data.resample('M').last()
            plt.plot(monthly_data['Adj Close'], label=self.ticker)
        elif type == 'year':
            yearly_data = self.data.resample('Y').last()
            plt.plot(yearly_data['Adj Close'], label=self.ticker)
        else:
            raise ValueError('수익률을 계산할 단위(day, month, year)가 잘못 입력되었습니다.')

        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Stock Price' + '(' + type + ')')
        plt.legend()
        plt.show()



if __name__ == '__main__':
    tickers = ['SPY', 'QQQ', 'VOO']

    stock_plotter = Chart(tickers, '2015-12-01', '2020-12-01')
    stock_plotter.plotstock(type='month')