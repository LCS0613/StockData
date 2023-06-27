# 주식 data를 활용한 수익률 계산 #
# Code written by LCS. 23.05.28 #

import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm


class Backtest:
    def __init__(self, ticker, start_date, end_date, dur_years, num_test):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.dur_years = dur_years
        self.num_test = num_test

        # 변수 설정(1년 = 252일)
        dur_days = int(252 * self.dur_years)

        # 결과 리스트 초기화
        self.return_results = []

        # 데이터 가져오기
        stockdata = yf.download(self.ticker, start=self.start_date, end=self.end_date)

        for _ in range(self.num_test):
            valid_range = len(stockdata) - dur_days  # Maximum valid index

            if valid_range <= 0:
                raise ValueError

            # 랜덤한 인덱스 선택
            random_index = np.random.randint(0, valid_range)

            # 선택한 인덱스에 해당하는 가격으로 주식 구매
            buy_price = stockdata.iloc[random_index]['Adj Close']

            # 일정기간(dur_years) 후 주식 판매
            sell_price = stockdata.iloc[random_index + dur_days]['Adj Close']

            # 수익률 계산 및 결과 저장(수익률은 1년단위 수익률으로 환산)
            returns = ((sell_price / buy_price) ** (1 / dur_years)) - 1
            self.return_results.append(returns)

    def calreturns(self):

        return self.return_results

    def calreturnav(self):
        returnav = np.mean(self.return_results)
        print('수익률 평균: ', round(returnav, 2) * 100, '%')

        return returnav

    def calreturnmed(self):
        returnmed = np.median(self.return_results)
        print('수익률 중간값: ', round(returnmed, 2) * 100, '%')

        return returnmed

    def calreturnstd(self):
        returnstd = np.std(self.return_results)
        print('수익률 표준편차: ', round(returnstd, 2) * 100)

        return returnstd


class Plotter:

    def __init__(self, results, dur_years, num_test):
        self.results = results   # 결과값(list)
        self.dur_years = dur_years
        self.num_test = num_test

    def plothist(self, plot_num):
        # 수익률 분포 히스토그램 그리기
        plt.figure(figsize=(10, 6))
        _, bins, _ = plt.hist(self.results[plot_num], bins=30, edgecolor='black', alpha=0.7, label='Simulation Results',
                              density=False)

        mu, sigma = norm.fit(self.results[plot_num])

        # 평균과 표준편차 표시
        plt.axvline(mu, color='b', linestyle='--', linewidth=1.5, label='Mean')
        plt.axvline(mu + sigma, color='g', linestyle='--', linewidth=1.5, label='Mean + Std Dev')
        plt.axvline(mu - sigma, color='g', linestyle='--', linewidth=1.5, label='Mean - Std Dev')

        # Y축 레이블 변경 (확률밀도(%)로 표시)
        plt.ylabel('Probability Density')

        # 그래프 설정
        plt.xlabel('Returns')
        plt.title('Simulation Results: ' + str(self.dur_years[plot_num]) + '-Year Returns' +
                  ' (Test: ' + str(self.num_test) + ')')
        plt.legend()

        plt.show()

    def plotcdf(self):
        plt.figure(figsize=(10, 6))

        for i, self.dur_years in enumerate(self.dur_years):
            mu, sigma = norm.fit(self.results[i])
            x = np.linspace(min(self.results[i]), max(self.results[i]), 100)
            cdf = norm.cdf(x, mu, sigma)

            plt.plot(x, cdf, label=str(self.dur_years) + '-Year')

        # Y축 레이블 변경 (누적 확률로 표시)
        plt.ylabel('Cumulative Probability')

        # 그래프 설정
        plt.xlabel('Returns')
        plt.title('Simulation Results (Test: ' + str(self.num_test) + ')')
        plt.legend()

        plt.show()



if __name__ == '__main__':
    start_date = '2003-01-01'
    end_date = '2023-01-21'
    ticker = 'AAPL'
    num_test = 10000

    dur_years_list = [1, 2, 3, 4, 5, 10]
    results_list = []

    for dur_years in dur_years_list:
        backtest = Backtest(ticker, start_date, end_date, dur_years, num_test)
        backtest.calreturnmed()
        backtest.calreturnstd()
        results_list.append(backtest.calreturns())

    plotter = Plotter(results_list, dur_years_list, num_test)
    plotter.plotcdf()
    #plotter.plothist(5)
