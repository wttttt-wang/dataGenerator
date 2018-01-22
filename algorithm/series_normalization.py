from sklearn.preprocessing import MinMaxScaler, normalize
import numpy as np


def simple_min_max(data):
    scaler = MinMaxScaler()
    transed = scaler.fit_transform(data)
    return transed


def normed(data):
    normVal = normalize(data)
    return normVal


if __name__ == "__main__":
    data = [[1., -1., 2.]]
    print normed(data)
    print normed([[109, 283, 921]])
