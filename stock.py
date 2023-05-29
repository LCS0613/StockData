# 주식 data를 활용한 수익률 계산 #
# Code written by LCS. 23.05.28 #

import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm


# 과거데이터 기준으로 1년단위 수익률 계산
def calreturn(ticker, start_date, end_date, dur_years, num_test):
    # 변수 설정(1년 = 252일)
    dur_days = int(252 * dur_years)

    # 결과 리스트 초기화
    return_results = []

    # 데이터 가져오기
    stockdata = yf.download(ticker, start=start_date, end=end_date)

    for _ in range(num_test):
        # 랜덤한 인덱스 선택
        random_index = np.random.randint(0, len(stockdata) - dur_days)

        # 선택한 인덱스에 해당하는 가격으로 주식 구매
        buy_price = stockdata.iloc[random_index]['Close']

        # 일정기간(dur_years) 후 주식 판매
        sell_price = stockdata.iloc[random_index + dur_days]['Close']

        # 수익률 계산 및 결과 저장(수익률은 1년단위 수익률으로 환산)
        returns = ((sell_price / buy_price) ** (1 / dur_years)) - 1
        return_results.append(returns)

    print(start_date, ' 부터', end_date, ' 까지', '임의의 시점에서 주식구매 한 뒤', dur_years, '년 후 팔았을 때')
    print('수익률 평균: ', round(np.mean(return_results), 2) * 100, '%')
    print('수익률 중간값: ', round(np.median(return_results), 2) * 100, '%')
    print('수익률 표준편차: ', round(np.std(return_results), 2) * 100)

    return return_results


def plothist(results, dur_years, num_test):
    # 수익률 분포 히스토그램 그리기
    plt.figure(figsize=(10, 6))
    _, bins, _ = plt.hist(results, bins=30, edgecolor='black', alpha=0.7, label='Simulation Results',
                                     density=False)

    mu, sigma = norm.fit(results)

    # 평균과 표준편차 표시
    plt.axvline(mu, color='b', linestyle='--', linewidth=1.5, label='Mean')
    plt.axvline(mu + sigma, color='g', linestyle='--', linewidth=1.5, label='Mean + Std Dev')
    plt.axvline(mu - sigma, color='g', linestyle='--', linewidth=1.5, label='Mean - Std Dev')

    # Y축 레이블 변경 (확률밀도(%)로 표시)
    plt.ylabel('Probability Density')

    # 그래프 설정
    plt.xlabel('Returns')
    plt.title('Simulation Results: ' + str(dur_years) + '-Year Returns' + ' (Test: ' + str(num_test) + ')')
    plt.legend()

    plt.show()

def plotcdf(results, dur_years, num_test):
    # 수익률 분포 히스토그램 그리기
    plt.figure(figsize=(10, 6))

    mu, sigma = norm.fit(results)

    # 누적 확률 밀도 함수(CDF) 그래프 그리기
    x = np.linspace(min(results), max(results), 100)
    cdf = norm.cdf(x, mu, sigma)
    plt.plot(x, cdf, 'r', linewidth=2, label='CDF')

    # 평균과 표준편차 표시
    plt.axvline(mu, color='b', linestyle='--', linewidth=1.5, label='Mean')
    plt.axvline(mu + sigma, color='g', linestyle='--', linewidth=1.5, label='Mean + Std Dev')
    plt.axvline(mu - sigma, color='g', linestyle='--', linewidth=1.5, label='Mean - Std Dev')

    # Y축 레이블 변경 (누적 확률로 표시)
    plt.ylabel('Cumulative Probability')

    # 그래프 설정
    plt.xlabel('Returns')
    plt.title('Simulation Results: ' + str(dur_years) + '-Year Returns' + ' (Test: ' + str(num_test) + ')')
    plt.legend()

    plt.show()



if __name__ == '__main__':
    start_date = '2015-05-23'
    end_date = '2023-05-23'
    ticker = 'SPY'
    dur_years = 1
    num_test = 1000

    test_result = calreturn(ticker, start_date, end_date, dur_years, num_test)
    print(test_result)
    plotcdf(test_result, dur_years, num_test)
