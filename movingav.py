# 가격이동평균(moving average) 전략 백테스팅
# Code written by LCS. 23.06.22 #

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# download_data : 주가 데이터 다운로드
def download_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# plot_evaluated_value : 주가 그래프 출력(라인차트)
def plot_evaluated_value(data, ticker):
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Close'], label=f'{ticker} Price')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'{ticker} Price over Time')
    plt.legend()
    plt.show()

# plot_strategy_evaluated_value : 이동평균 적용한 그래프 출력
def plot_strategy_evaluated_value(data, ma_data, ticker):
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Close'], label=f'{ticker} Price')
    plt.plot(ma_data.index, ma_data['strategy_cum_returns'] * data.iloc[0]['Close'], label='Moving Average Strategy')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'{ticker} Price and Moving Average Strategy over Time')
    plt.legend()
    plt.show()

# calculate_returns : 수익률 계산(일별)
def calculate_returns(data):
    data['daily_returns'] = data['Close'].pct_change()
    data = data.dropna()    # 데이터 결측치 제거
    return data

# calculate_return_with_investment : 수익률 계산
def calculate_return_with_investment(data, investment):
    data_with_returns = calculate_returns(data)
    end_price = data_with_returns.iloc[-1]['Close']
    end_value = investment * (1 + data_with_returns['daily_returns']).cumprod().iloc[-1]
    return end_price, end_value

# ma_strategies : 이동평균전략
def ma_strategies(data, investment):
    data_with_returns = calculate_returns(data)

    # 단기이동평균과 장기이동평균 정의
    ma_short = data_with_returns['Close'].rolling(10).mean()
    ma_long = data_with_returns['Close'].rolling(60).mean()

    # 매수 시그널(골든크로스), 매도 시그널(데드크로스) 정의
    buy_signal = (ma_short > ma_long) & (ma_short.shift() < ma_long.shift())
    sell_signal = (ma_short < ma_long) & (ma_short.shift() > ma_long.shift())

    ma_data = pd.concat([data_with_returns['Close'], ma_short, ma_long], axis=1)
    ma_data.columns = ['Price', 'ma_short', 'ma_long']
    ma_data['buy_signal'] = buy_signal
    ma_data['sell_signal'] = sell_signal
    ma_data['pct_change'] = ma_data['Price'].pct_change()

    ma_data['in_position'] = False

    previous_position = False
    for index, row in ma_data.iterrows():
        if row['buy_signal']:
            ma_data.loc[index, 'in_position'] = True
            previous_position = True
        elif row['sell_signal']:
            ma_data.loc[index, 'in_position'] = True
            previous_position = False
        else:
            ma_data.loc[index, 'in_position'] = previous_position

    ma_data['strategy_returns'] = ma_data['pct_change'] * ma_data['in_position']
    ma_data['strategy_cum_returns'] = (1 + ma_data['strategy_returns']).cumprod()
    ma_returns = ma_data['strategy_cum_returns'].iloc[-1]

    end_price, end_value = calculate_return_with_investment(data, investment)
    hold_returns = (end_value - investment) / investment

    return ma_data, ma_returns, hold_returns


def plot_moving_averages(data, ma_data, ticker):
    plt.figure(figsize=(16, 8))
    plt.plot(data.index, data['Close'], label=f'{ticker} Price')
    plt.plot(ma_data.index, ma_data['ma_short'], label='Short Term Moving Average (10 days)')
    plt.plot(ma_data.index, ma_data['ma_long'], label='Long Term Moving Average (60 days)')

    buy_signals = ma_data[ma_data['buy_signal']].index
    sell_signals = ma_data[ma_data['sell_signal']].index

    plt.scatter(buy_signals, [data.loc[date]['Close'] for date in buy_signals], marker='^', color='g', s=100,
                label="Buy Signal")
    plt.scatter(sell_signals, [data.loc[date]['Close'] for date in sell_signals], marker='v', color='r', s=100,
                label="Sell Signal")

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'{ticker} Price with Moving Averages and Buy/Sell Signals')
    plt.legend()
    plt.show()

def run(ticker, start_date, end_date, investment):
    # 데이터 다운로드 및 평가금액 계산
    data = download_data(ticker, start_date, end_date)
    end_price, end_value = calculate_return_with_investment(data, investment)

    # 평가금액 그래프 출력
    plot_evaluated_value(data, ticker)

    # 종료일 평가금액 출력
    print("종료일 가격: ${:.2f}".format(end_price))
    print("초기 투자금액: ${:.2f}".format(investment))
    print("종료일 평가금액: ${:.2f}".format(end_value))

    # 이동평균 전략, 초기 투자 후 보유 비교 결과 반환
    ma_data, ma_returns, hold_returns = ma_strategies(data, investment)

    # 이동평균 전략 평가금액 그래프 출력
    plot_strategy_evaluated_value(data, ma_data, ticker)

    # 결과 출력
    print("이동평균 전략 누적 수익률: {:.2f}%".format((ma_returns - 1) * 100))
    print("초기 투자 후 보유 누적 수익률: {:.2f}%".format(hold_returns * 100))


if __name__ == '__main__':
    data = download_data('SPY', '2015-01-01', '2018-01-01')
    ma_data, _, _ = ma_strategies(data, 1000)
    run('EPAM', '2019-01-01', '2023-01-01', 1000)
    plot_moving_averages(data, ma_data, 'SPY')
