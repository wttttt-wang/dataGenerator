# Normalize time series data
from pandas import Series
from sklearn.preprocessing import MinMaxScaler


def simple_min_max(series):
    # load the dataset and print the first 5 rows
    # prepare data for normalization
    values = array(series).reshape((len(values), 1))
    # train the normalization
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler = scaler.fit(values)
    print('Min: %f, Max: %f' % (scaler.data_min_, scaler.data_max_))
    # normalize the dataset and print the first 5 rows
    normalized = scaler.transform(values)
    for i in range(5):
        print(normalized[i])
    # inverse transform and print the first 5 rows
    inversed = scaler.inverse_transform(normalized)
    for i in range(5):
        print(inversed[i])