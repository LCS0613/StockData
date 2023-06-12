# 정액적립식매수방법에 의한 수익률 계산 #
# Dollar-cost averaging investment #
# Code written by LCS. 23.05.28 #


import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


class Costaveraging():

    def __init__(self, ticker, start_date, end_date, invest, period):
        # ticker : 주식호칭. ticker
        # start_date : 계산 시작날짜('yyyy-mm-dd' 형식)
        # end_date : 계산 종료날짜('yyyy-mm-dd' 형식)
        # invest : 투자금. 투자주기별로 납입하는 금액
        # period : 투자금 납입 주기
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.invest = invest
        self.period = period

        # 일수 계산
        start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
        num_days = (end_date - start_date).days

        # 주간 매수 금액 계산
        self.num_periods = int(num_days / self.period) + 1

        # 데이터 가져오기 (including one period before the specified start date)
        self.start_date_with_offset = datetime.strptime(self.start_date, '%Y-%m-%d') - timedelta(days=self.period)
        self.stockdata = yf.download(self.ticker, start=self.start_date_with_offset, end=self.end_date)

        # 날짜 설정
        self.start_date_strp = datetime.strptime(self.start_date, '%Y-%m-%d')
        self.end_date_strp = datetime.strptime(self.end_date, '%Y-%m-%d')

    # 정액적립식 투자결과를 데이터프레임 형태로 나타내기
    def ca_df(self):
        result = []

        # 주식 개수 초기화
        count = 0

        test = self.stockdata
        # 주별로 주식 매수
        for i in range(self.num_periods):
            try:
                # 시작일로부터 몇 번째 날짜인지 계산하여 1을 뺀 값 반환
                target_date = self.start_date_strp + timedelta(days=self.period * i)
                index = self.stockdata.index.get_loc(target_date)
                buy_price = self.stockdata.iloc[index]['Adj Close']
                count = count + self.invest / buy_price

                # 해당 기간의 보유 주식 개수, 평가금액, 수익률을 DataFrame에 추가
                eval_value = count * self.stockdata.iloc[index]['Adj Close']
                returns = round(eval_value / ((i + 1) * self.invest) - 1, 3)
                temp_list = [target_date, count, eval_value, returns]
                result.append(temp_list)
            except KeyError:
                j = 1
                # 주말이거나 데이터가 없는 경우, 전 날짜의 종가에 투자
                target_date = self.start_date_strp + timedelta(days=self.period*i-j)
                while target_date not in self.stockdata.index:
                    j = j + 1
                    target_date = self.start_date_strp + timedelta(days=self.period * i - j)
                buy_price = self.stockdata.loc[target_date]['Adj Close']
                count = count + self.invest / buy_price

                # 해당 기간의 보유 주식 개수, 평가금액을 DataFrame에 추가
                eval_value = count * self.stockdata.loc[target_date]['Adj Close']
                returns = round(eval_value / ((i + 1) * self.invest) - 1, 3)
                temp_list = [target_date, count, eval_value, returns]
                result.append(temp_list)

        df = pd.DataFrame(result, columns=['Date', 'Shares Held', 'Evaluation', 'Returns'])

        # 결과 반환
        return df

    # 주간 정액적립식 투자수익률 계산
    def ca_return(self):

        # 수익률 이력 데이터 불러오기
        ca_data = self.ca_df()

        # 총 투자금액 계산
        total_investment = self.num_periods * self.invest

        # 최종 평가금액
        final_value = ca_data.iloc[-1]['Evaluation']

        # 최종 수익률
        returns = ca_data.iloc[-1]['Returns']

        # 1년 단위 수익률
        num_years = (self.end_date_strp - self.start_date_strp).days / 365
        returns_per_year = ((final_value / total_investment) ** (1 / num_years)) - 1

        # 결과 프린트
        print('계산(종료) 날짜 : ', ca_data.iloc[-1]['Date'])
        print('총 투자금액 : ', total_investment, '$')
        print('최종 평가금액 : ', final_value, '$')
        print('총 수익률 : ', round(returns * 100, 2), '%')
        print('1년단위 수익률 : ', round(returns_per_year * 100, 2), '%')

        # 결과 반환
        return total_investment, final_value, returns, returns_per_year


if __name__ == '__main__':
    spy = Costaveraging('QQQ', '2010-03-01', '2023-05-01', 100, 7)
    print(spy.ca_df())
    print(spy.ca_return())