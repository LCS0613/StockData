# 아이슈타인의 72의 법칙을 수치적으로 증명
import math
import matplotlib.pyplot as plt
import numpy as np

def caltime_real(rate):
    y = math.log(2) / math.log(1 + rate / 100)
    return y

def caltime_72r(rate):
    y = 72 / rate
    return y

def calculate_error(real_values, rule72_values):
    errors = [abs(real - rule72) / real * 100 for real, rule72 in zip(real_values, rule72_values)]
    return errors

def calvalue(rate):
    y = math.log(2) / math.log(1 + rate / 100) * rate
    return y

if __name__ == '__main__':
    rates = np.linspace(1, 50, 100)  # 0.1부터 10까지 이자율 범위로 100개의 값을 생성
    real_times = [caltime_real(rate) for rate in rates]  # 실제 시간 계산
    rule72_times = [caltime_72r(rate) for rate in rates]  # 72의 법칙 시간 계산
    errors = calculate_error(real_times, rule72_times)  # 오차율 계산

    # 실제시간과 72의 법칙 그래프 비교
    plt.plot(rates, real_times, 'r', label='Real Time')  # 실제 시간 그래프 (빨간색)
    plt.plot(rates, rule72_times, 'b', label='Rule of 72 Time')  # 72의 법칙 시간 그래프 (파란색)
    plt.xlabel('Interest Rate (%)')  # x축 레이블 설정
    plt.ylabel('Elapsed Time (years)')  # y축 레이블 설정
    plt.title('Elapsed Time vs. Interest Rate')  # 그래프 제목 설정
    plt.legend()  # 범례 표시
    plt.grid(True)  # 그리드 표시
    plt.show()  # 그래프 출력

    # 오차율 그래프
    plt.plot(rates, errors, 'b', label='Error Percentage')  # 오차율 그래프 (파란색)
    plt.xlabel('Interest Rate (%)')  # x축 레이블 설정
    plt.ylabel('Error Percentage (%)')  # y축 레이블 설정
    plt.title('Error Percentage vs. Interest Rate')  # 그래프 제목 설정
    plt.legend()  # 범례 표시
    plt.grid(True)  # 그리드 표시
    plt.show()  # 그래프 출력

    # 72 대신 정확한 값을 찾기위한 그래프
    rates = np.linspace(0.1, 50, 100)  # 0.1부터 10까지 이자율 범위로 100개의 값을 생성
    values = [calvalue(rate) for rate in rates]  # 함수를 이용해 값을 계산

    plt.plot(rates, values, 'r', label='Test')  # 계산값 그래프 (빨간색)
    plt.xlabel('Interest Rate (%)')  # x축 레이블 설정
    plt.ylabel('Value')  # y축 레이블 설정
    plt.title('Calculation Result vs. Interest Rate')  # 그래프 제목 설정
    plt.legend()  # 범례 표시
    plt.grid(True)  # 그리드 표시
    plt.show()  # 그래프 출력