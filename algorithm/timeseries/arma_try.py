# -*- coding:utf-8 -*-
from statsmodels.tsa.stattools import adfuller
import pandas as pd
import matplotlib.pyplot as plt
from mysql import readData
import MySQLdb
from statsmodels.tsa.arima_model import ARMA
import numpy as np
from statsmodels.tsa.arima_model import ARIMA
from algorithm.series_normalization import *
import sys


def test_stationarity(timeseries):
    # station if p < 0.05
    print 'Results of Augment Dickey-Fuller Test:'
    dftest = adfuller(series, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value (%s)' % key] = value
    print dfoutput


def proper_model(data_ts, maxLag):
    """
    with given maxLag, iterate on p & q value, get the p&q with smallest fit error.
    :param data_ts:
    :param maxLag:
    :return:
    """
    best_p = 0
    best_q = 0
    best_bic = sys.maxint
    best_model = None
    for p in np.arange(maxLag):
        for q in np.arange(maxLag):
            model = ARMA(data_ts, order=(p, q))
            try:
                results_ARMA = model.fit(disp=-1)
            except:
                continue
            bic = results_ARMA.bic
            print p, q, bic, best_bic
            if bic < best_bic:
                best_p = p
                best_q = q
                best_bic = bic
                best_model = results_ARMA
    return best_p, best_q, best_model


def fit_ARMA(timeseries):
    rol_mean = timeseries.rolling(window=12).mean()
    rol_mean.dropna(inplace=True)
    ts_diff_1 = rol_mean.diff(1)
    from statsmodels.tsa.arima_model import ARMA
    model = ARMA(ts_diff_1, order=(1, 1))
    result_arma = model.fit(disp=-1, method='css')
    print result_arma


def plot_data(timeseries):
    dta = pd.Series(timeseries)
    plt.plot(dta)
    plt.show()


def fit_ARMA2(series):
    from statsmodels.tsa.arima_model import ARIMA
    # 定阶
    # 一般阶数不超过length/10
    pmax, qmax = int(len(series) / 10), int(len(series) / 10)
    # bic矩阵
    bic_matrix = []
    for p in range(pmax + 1):
        tmp = []
        for q in range(qmax + 1):
            # 存在部分报错，所以用try来跳过报错。
            try:
                tmp.append(ARIMA(series, (p, 1, q)).fit().bic)
            except:
                tmp.append(None)
        bic_matrix.append(tmp)
    # 从中可以找出最小值
    bic_matrix = pd.DataFrame(bic_matrix)
    # 先用stack展平，然后用idxmin找出最小值位置。
    p, q = bic_matrix.stack().idxmin()
    print(u'BIC最小的p值和q值为：%s、%s' % (p, q))

    model = ARIMA(series, (p, 1, q)).fit()
    print model.summary2()


def white_noise_detect(series):
    # 白噪声检验: if p < 0.05 则拒绝原假设，为非白噪声序列(95%的把握)
    from statsmodels.stats.diagnostic import acorr_ljungbox
    # 返回统计量和p值
    noiseRes = acorr_ljungbox(series, lags=1)
    print u'一阶差分序列的白噪声检验结果为：'
    print 'stat                  | p-value'
    for x in noiseRes:
        print x, '|',


def plot_correlation(series):
    # 自相关图
    from statsmodels.graphics.tsaplots import plot_acf
    plot_acf(series).show()
    plt.show()
    from statsmodels.graphics.tsaplots import plot_pacf
    # 偏自相关图
    plot_pacf(series).show()
    plt.show()


def ARIMA_model(series, p, d, q):
    from pandas import DataFrame
    model = ARIMA(series, order=(p, d, q))
    model_fit = model.fit(disp=0)
    print model_fit.summary()
    # plot residual errors
    residuals = DataFrame(model_fit.resid)
    residuals.plot()
    plt.show()
    residuals.plot(kind='kde')
    plt.show()
    print(residuals.describe())


def predict(X):
    from sklearn.metrics import mean_squared_error
    size = int(len(X) * 0.66)
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=(0, 1, 0))  # 7, 1, 1
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
        print('predicted=%f, expected=%f' % (yhat, obs))
    error = mean_squared_error(test, predictions)
    print('Test MSE: %.3f' % error)
    # plot
    plt.plot(test)
    plt.plot(predictions, color='red')
    plt.show()


if __name__ == '__main__':
    conn = MySQLdb.connect(user='root', db='paperData')
    series = readData.getMetrics(conn, 'usedHeapMem', 'container_1513994030877_0149_01_000002')
    for i in range(len(series)):
        series[i] *= 1.0
    # series = normed([series])[0]
    print len(series), series

    # print test_stationarity(series)
    # plot_correlation(series)
    # white_noise_detect(series)
    # plot_data(series)
    # print test_stationarity(series)
    # print proper_model(series, 20)
    ARIMA_model(series, 1, 1, 1)
    predict(series)
