from sklearn.preprocessing import MinMaxScaler, normalize
import numpy as np


def simple_min_max(data):
    scaler = MinMaxScaler()
    transed = scaler.fit_transform(data)
    return transed


def normed(data):
    normVal = normalize(data)
    return normVal


def interval_sampling(data, num):
    """
    :param data: origin data for sampling
    :param num: number of elements to return
    :return:
    """
    res = []
    interval, cnt, base = len(data) / num, 0, 0
    while cnt < num:
        res.append(data[base])
        cnt += 1
        base += interval
    return res


if __name__ == "__main__":
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print interval_sampling(data, 5)
